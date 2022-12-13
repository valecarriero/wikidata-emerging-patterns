#! /bin/bash
CODE_DIRECTORY=$(pwd)
read -p "Enter the absolute path of the folder where you want to store the results: " OUTPUTPATH
read -p "Enter the absolute path of the KGTK tsv edgefile of your domain KG: " EDGEFILE
read -p "Enter the absolute path of the KGTK tsv nodefile / labelfile of your domain KG: " NODEFILE
read -p "Enter the absolute path of the KGTK tsv edgefile containing P279star triples: " P279STARFILE
read -p "Enter the absolute path of the KGTK tsv edgefile containing all type P31 assertions (including the objects in your domain KG): " ALLEDGES
read -p "Enter a value [0, 1] that will be used for defining a threshold for selecting the most common classes. 0 means that only the most common class will be selected, 1 that all classes will be selected: " K
read -p "Enter a value [0, 1] that will be used for defining a threshold for selecting the most common properties per class. 0 means that only the most common property will be selected, 1 that all properties will be selected: " K2
read -p "Enter a value [0, 1] that will be used for defining a threshold for selecting the most common ranges per property per class. 0 means that only the most common range will be selected, 1 that all ranges will be selected: " K3

THRESHOLDS="$K$K2$K3"
FINALTHRESHOLDS=${THRESHOLDS//./}

mkdir $OUTPUTPATH/output
export kypher="kgtk --debug query"
### I generate a file that counts all instances of all classes: output tsv file
$kypher -i $EDGEFILE -o $OUTPUTPATH/output/classes.tsv --match  '(instance)-[:P31]->(class)' --return 'class as class, count(distinct instance) as count' --order-by 'count desc'
kgtk add-labels --input-file $OUTPUTPATH/output/classes.tsv --label-file $NODEFILE --output-file $OUTPUTPATH/output/classes.tsv

CLASSES_TSV=$(python -W ignore return_filtered_distribution.py --input_file $OUTPUTPATH/output/classes.tsv --k_value $K --output_folder $OUTPUTPATH/output)

COUNTINSTANCES=$($kypher -i $EDGEFILE --match '(instance)-[:P31]->(class)' --return 'count(distinct instance) as count')
TOTINSTANCES=$(echo $COUNTINSTANCES | cut -d' ' -f 2)

# add percentages to both the file with all classes and the file with filtered classes
python -W ignore add_percentage_classes.py --input_tsv $OUTPUTPATH/output/classes.tsv --tot $TOTINSTANCES
python -W ignore add_percentage_classes.py --input_tsv $CLASSES_TSV --tot $TOTINSTANCES

echo "the file with the most populated classes based on the threshold has been created:"
echo $CLASSES_TSV
SUBGRAPHS_FOLDER=$OUTPUTPATH/output/all_subgraphs
mkdir $SUBGRAPHS_FOLDER
python extract_subgraphs.py --classes_tsv $CLASSES_TSV --output_folder $SUBGRAPHS_FOLDER --edgefile $EDGEFILE --p279starfile $P279STARFILE

### run file with kgtk commands for generating a file containing a subgraph for each selected class
chmod +x subgraphs_KGTKcommands.sh
./subgraphs_KGTKcommands.sh

mkdir $OUTPUTPATH/output/patterns

cd $SUBGRAPHS_FOLDER
### generate a file with all properties for each selected class
for FILE in *.gz
	do
		CLASS=$(echo $FILE | cut -d'.' -f 1)
		mkdir ../patterns/$CLASS
		$kypher -i $FILE -o ../patterns/$CLASS/$CLASS-properties.tsv --match '(class)<-[:P31]-(instance)-[p]->()' --where 'p.label != "P31" and p.label != "P279"' --return 'distinct p.label as property, count(distinct instance) as count' --order-by 'count desc'
		kgtk add-labels --input-file ../patterns/$CLASS/$CLASS-properties.tsv --label-file $NODEFILE --output-file ../patterns/$CLASS/$CLASS-properties.tsv

		python -W ignore $CODE_DIRECTORY/add_percentage_properties_dr.py --input_tsv ../patterns/$CLASS/$CLASS-properties.tsv --clas_tsv $CLASSES_TSV --clas $CLASS

done

### generate a file with domain and ranges pairs
#COUNTER=1
QUOTE=\'
for FILE in *.gz
	do
		CLASS=$(echo $FILE | cut -d'.' -f 1)
		echo $CLASS

		TEMP_FOLDER=$OUTPUTPATH/output/patterns/$CLASS/temp
		mkdir $TEMP_FOLDER

		### partial file without datatype ranges
		$kypher -i $FILE -i $ALLEDGES -o ../patterns/$CLASS/$CLASS-dr-pairs-nodatatype.tsv --match '(domain)<-[:P31]-(s)-[p]->(o), z: (o)-[:P31]->(range)' --where 'p.label != "P31" and p.label != "P279"' --return 'distinct domain as domain, p.label as property, range as range, count(distinct s) as count' --order-by 'property, count desc'
		
		### node file with all ranges (both entities and datatypes)
		$kypher -i $FILE -o ../patterns/$CLASS/$CLASS-all-ranges.tsv --match '(domain)<-[:P31]-(s)-[p]->(o)' --where 'p.label != "P31" and p.label != "P279"' --return 'distinct o as id'

		### node file with only ranges with :P31
		$kypher -i $FILE -i $ALLEDGES -o ../patterns/$CLASS/$CLASS-typed-ranges.tsv --match '(domain)<-[:P31]-(s)-[p]->(o), z: (o)-[:P31]->(range)' --where 'p.label != "P31" and p.label != "P279"' --return 'distinct o as id'

		### filter the first file with the second one -> obtain a node file with only datatypes
		kgtk ifnotexists --input-file ../patterns/$CLASS/$CLASS-all-ranges.tsv --filter-on ../patterns/$CLASS/$CLASS-typed-ranges.tsv --o ../patterns/$CLASS/$CLASS-datatype-ranges.tsv
		
		### separate "real" datatypes and Qentities that are not typed (i.e. missing P31)
		python -W ignore $CODE_DIRECTORY/filter_Q_notQ_wd_entities.py ../patterns/$CLASS/$CLASS-datatype-ranges.tsv ../patterns/$CLASS/$CLASS-Q-datatype-ranges.tsv ../patterns/$CLASS/$CLASS-notQ-datatype-ranges.tsv
		
		### obtain an edge file with only datatypes
		kgtk ifexists --input-file $FILE --filter-on ../patterns/$CLASS/$CLASS-notQ-datatype-ranges.tsv -o ../patterns/$CLASS/$CLASS-subgraph-onlydatatype.tsv.gz --input-keys node2
		
		ONLYDATATYPESUBGRAPH=../patterns/$CLASS/$CLASS-subgraph-onlydatatype.tsv.gz


		### partial file with only datatype ranges
		$kypher -i $ONLYDATATYPESUBGRAPH -i $FILE -o ../patterns/$CLASS/$CLASS-dr-pairs-datatype.tsv --match '(s)-[p]->(o {wikidatatype: type}), z: (s)-[:P31]->(domain)' --return 'distinct domain as domain, p.label as property, type as range, count(distinct s) as count' --order-by 'property, count desc'

		python -W ignore $CODE_DIRECTORY/merge_nodatatype_yesdatatype.py --nodp_tsv ../patterns/$CLASS/$CLASS-dr-pairs-nodatatype.tsv --yesdp_tsv ../patterns/$CLASS/$CLASS-dr-pairs-datatype.tsv --output_file ../patterns/$CLASS/$CLASS-dr-pairs.tsv
		kgtk add-labels --input-file ../patterns/$CLASS/$CLASS-dr-pairs.tsv --label-file $NODEFILE --output-file ../patterns/$CLASS/$CLASS-dr-pairs.tsv
#		COUNTER=$[$COUNTER +1]

		mv ../patterns/$CLASS/$CLASS-dr-pairs-nodatatype.tsv $TEMP_FOLDER
		mv ../patterns/$CLASS/$CLASS-all-ranges.tsv $TEMP_FOLDER
		mv ../patterns/$CLASS/$CLASS-typed-ranges.tsv $TEMP_FOLDER
		mv ../patterns/$CLASS/$CLASS-datatype-ranges.tsv $TEMP_FOLDER
		mv ../patterns/$CLASS/$CLASS-Q-datatype-ranges.tsv $TEMP_FOLDER
		mv ../patterns/$CLASS/$CLASS-notQ-datatype-ranges.tsv $TEMP_FOLDER
		mv ../patterns/$CLASS/$CLASS-dr-pairs-datatype.tsv $TEMP_FOLDER
		mv $ONLYDATATYPESUBGRAPH $TEMP_FOLDER

done

### going back to code folder
cd $CODE_DIRECTORY

### for each file with all properties for each selected class, I run the kgtk commands for returning the most common properties based on a threshold
for FOLDER in $OUTPUTPATH/output/patterns/*
	do
		#CLASS=$(echo $FOLDER | cut -d'/' -f 3)
		CLASS=${FOLDER##*/}
		echo $CLASS		
		#echo $FOLDER
		for FILE in $FOLDER/*properties.tsv
			do
				#echo $FILE
	    		PROP_TSV=$(python -W ignore return_filtered_distribution.py --input_file $FILE --k_value $K2 --output_folder $FOLDER)
	    		#echo $PROP_TSV
	    		kgtk add-labels --input-file $PROP_TSV --label-file $NODEFILE --output-file $PROP_TSV
	    		# i filter the dr pairs file with the most common properties
	    		FILTERED_DR_TSV=$(python -W ignore filter_drpairs_basedon_properties.py --dr_pairs $FOLDER/$CLASS-dr-pairs.tsv --filtered_properties $PROP_TSV --output_folder $FOLDER/$CLASS)
		    	# i filter the new dr pairs file with the most common ranges
		    	FILTERED_RANGE_TSV=$(python -W ignore filter_drpairs_basedon_filtered_distribution.py --clas $CLASS --input_file $FILTERED_DR_TSV --k_value $K3 --output_folder $FOLDER)
		    	python -W ignore add_percentage_properties_dr.py --input_tsv $FILTERED_RANGE_TSV --clas_tsv $CLASSES_TSV --clas $CLASS

	    done
done

