import pandas as pd
import argparse

def extract_subgraphs(classes_tsv, output_folder, edgefile, p279starfile):

	classes_df = pd.read_csv(classes_tsv, delimiter="\t")

	subgraphs_commands = []

	for index, row in classes_df.iterrows():
		#command = "$kypher -i " + edgefile + " -o " + output_folder + "/" + row["class"] + ".tsv.gz --match '(n2 {wikidatatype: type})<-[l {label: property}]-(n1)-[:P31]->(:" + row["class"] + ")' --return 'l as id, n1 as node1, property as label, n2 as node2, type'"
		command = "$kypher -i " + edgefile + " -i " + p279starfile + " -o " + output_folder + "/" + row["class"] + ".tsv.gz --match '(n2 {wikidatatype: type})<-[l {label: property}]-(n1)-[:P31]->(class), z: (class)-[:P279star]->(:" + row["class"] + ")' --return 'l as id, n1 as node1, property as label, n2 as node2, type'"

		subgraphs_commands.append(command)

	with open('subgraphs_KGTKcommands.sh', 'w') as f:
		f.write("#! /bin/bash" + "\n")
		for command in subgraphs_commands:
			f.write(command + "\n")


if __name__ == '__main__':
	parser = argparse.ArgumentParser()

	# Parameters
	parser.add_argument('--classes_tsv', type=str, required=True)
	parser.add_argument('--output_folder', type=str, required=True)
	parser.add_argument('--edgefile', type=str, required=True)
	parser.add_argument('--p279starfile', type=str, required=True)

	args = parser.parse_args()
    
	extract_subgraphs(args.classes_tsv, args.output_folder, args.edgefile, args.p279starfile)