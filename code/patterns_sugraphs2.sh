#! /bin/bash

read -p "Enter the absolute path of the KGTK tsv edgefile of your domain KG: " EDGEFILE
read -p "Enter the absolute path of the KGTK tsv nodefile / labelfile of your domain KG: " NODEFILE
mkdir output
export kypher="kgtk --debug query --graph-cache wikidata.sqlite3.db"
### I generate a file that counts all instances of all classes: output tsv file
$kypher -i $EDGEFILE -o output/classes.tsv --match  '(instance)-[:P31]->(class)' --return 'class as class, count(distinct instance) as count' --order-by 'count desc'
kgtk add-labels --input-file output/classes.tsv --label-file $NODEFILE --output-file output/classes.tsv
read -p "Enter a value [0, 1] that will be used for defining a threshold for selecting the most common classes. 0 means that only the most common class will be selected, 1 that all classes will be selected: " K
CLASSES_TSV=$(python -W ignore return_filtered_distribution.py --input_file output/classes.tsv --k_value $K --output_folder output/)
echo "the file with the most populated classes based on the threshold has been created:"
echo $CLASSES_TSV
SUBGRAPHS_FOLDER="output/all_subgraphs"
mkdir $SUBGRAPHS_FOLDER
python extract_subgraphs.py --classes_tsv $CLASSES_TSV --output_folder $SUBGRAPHS_FOLDER --edgefile $EDGEFILE

### run file with kgtk commands for generating a file containing a subgraph for each selected class
chmod +x subgraphs_KGTKcommands.sh
./subgraphs_KGTKcommands.sh

mkdir output/patterns
cd $SUBGRAPHS_FOLDER
### generate a file with all properties for each selected class
for FILE in *
	do
		CLASS=$(echo $FILE | cut -d'.' -f 1)
		mkdir ../patterns/$CLASS
		$kypher -i $FILE -o ../patterns/$CLASS/$CLASS-properties.tsv --match '(instance)-[p]->()' --where 'p.label != "P31" and p.label != "P279"' --return 'distinct p.label as property, count(distinct instance) as count' --order-by 'count desc'
		kgtk add-labels --input-file ../patterns/$CLASS/$CLASS-properties.tsv --label-file $NODEFILE --output-file ../patterns/$CLASS/$CLASS-properties.tsv
done

read -p "Enter the absolute path of the KGTK tsv edgefile containing all triples (e.g. including type assertions of objects in your domain KG). Can be also the same as the previous edgefile: " ALLEDGES

### generate a file with domain and ranges pairs
COUNTER=1
QUOTE=\'
for FILE in *
	do
		CLASS=$(echo $FILE | cut -d'.' -f 1)
		### partial file without datatype ranges
		kgtk --debug query -i $FILE --as DKG -i $ALLEDGES --as ALL -o ../patterns/$CLASS/$CLASS-dr-pairs-nodatatype.tsv --match 'DKG: (domain)<-[:P31]-(s)-[p]->(o), ALL: (o)-[:P31]->(range)' --where 'p.label != "P31" and p.label != "P279"' --return 'distinct domain as domain, p.label as property, range as range, count(distinct s) as count' --order-by 'property, count desc'
		### node file with all ranges (both entities and datatypes)
		$kypher -i DKG -o ../patterns/$CLASS/$CLASS-all-ranges.tsv --match '(domain)<-[:P31]-(s)-[p]->(o)' --where 'p.label != "P31" and p.label != "P279"' --return 'distinct o as id'
		### node file with only ranges with :P31
		$kypher -i DKG -i ALL -o ../patterns/$CLASS/$CLASS-typed-ranges.tsv --match 'DKG: (domain)<-[:P31]-(s)-[p]->(o), ALL: (o)-[:P31]->(range)' --where 'p.label != "P31" and p.label != "P279"' --return 'distinct o as id'
		### filter the first file with the second one -> obtain a node file with only datatypes
		kgtk ifnotexists --input-file ../patterns/$CLASS/$CLASS-all-ranges.tsv --filter-on ../patterns/$CLASS/$CLASS-typed-ranges.tsv --o ../patterns/$CLASS/$CLASS-datatype-ranges.tsv
		### separate "real" datatypes and Qentities that are not typed (i.e. missing P31)
		python -W ignore ../../filter_Q_notQ_wd_entities.py ../patterns/$CLASS/$CLASS-datatype-ranges.tsv ../patterns/$CLASS/$CLASS-Q-datatype-ranges.tsv ../patterns/$CLASS/$CLASS-notQ-datatype-ranges.tsv
		### obtain an edge file with only datatypes
		kgtk ifexists --input-file DKG --filter-on ../patterns/$CLASS/$CLASS-notQ-datatype-ranges.tsv -o ../patterns/$CLASS/$CLASS-subgraph-onlydatatype.tsv.gz --input-keys node2
		### partial file with only datatype ranges
		$kypher -i ../patterns/$CLASS/$CLASS-subgraph-onlydatatype.tsv.gz --as SUBDKG -i DKG -o ../patterns/$CLASS/$CLASS-dr-pairs-datatype.tsv --match 'SUBDKG: (s)-[p]->(o {wikidatatype: type}), DKG: (s)-[:P31]->(domain)' --return 'distinct domain as domain, p.label as property, type as range, count(distinct s) as count' --order-by 'property, count desc'
		python -W ignore ../../merge_nodatatype_yesdatatype.py --nodp_tsv ../patterns/$CLASS/$CLASS-dr-pairs-nodatatype.tsv --yesdp_tsv ../patterns/$CLASS/$CLASS-dr-pairs-datatype.tsv --output_file ../patterns/$CLASS/$CLASS-dr-pairs.tsv
		COUNTER=$[$COUNTER +1]
done

read -p "Enter a value [0, 1] that will be used for defining a threshold for selecting the most common properties per class. 0 means that only the most common property will be selected, 1 that all properties will be selected: " K2
### going back to code folder
cd ../..

### for each file with all properties for each selected class, I run the kgtk commands for returning the most common properties based on a threshold (max deviation)
for FOLDER in output/patterns/*
	do
		echo $FOLDER
		## e.g. output/patterns/Q105543609
		for FILE in $FOLDER/*
			do
				echo $FILE
				# e.g. output/patterns/Q105543609/Q105543609-properties.tsv
	    		PROP_TSV=$(python -W ignore return_filtered_distribution.py --input_file $FILE --k_value $K2 --output_folder $FOLDER)
	    		kgtk add-labels --input-file PROP_TSV --label-file $NODEFILE --output-file PROP_TSV
	    done
done

