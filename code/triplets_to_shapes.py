import pandas as pd
import re as re
import argparse

def triplets_to_shapes(properties_input_tsv, triplets_input_tsv, output_folder, topic, date_wikidata_dump, thresholds):


	properties_df = pd.read_csv(properties_input_tsv, delimiter="\t")

	triplets_df = pd.read_csv(triplets_input_tsv, delimiter="\t")
	# domain	property	range	count	domain;label	property;label	range;label

	domain_class = triplets_input_tsv.split("/")[-1].split("-")[0]

	domain_label = triplets_df["domain;label"][0].split("@")[0]

	output_shex = output_folder + "/" + domain_class + "_shape.shex"

	Q_props = set()


	topic_subkg = "wikidata_" + topic + "_subkg_" + date_wikidata_dump

	wikidata_kg = "wikidata_" + date_wikidata_dump


	with open(output_shex, "a") as shex:
		shex.write("PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> " + "\n")
		shex.write("PREFIX wd: <http://www.wikidata.org/entity/> " + "\n")
		shex.write("PREFIX wdt: <http://www.wikidata.org/prop/direct/> " + "\n")
		shex.write("PREFIX wikibase: <http://wikiba.se/ontology#> " + "\n")
		shex.write("PREFIX dcterms: <http://purl.org/dc/terms/> " + "\n")
		shex.write("PREFIX os: <http://w3id.org/owlstar/> " + "\n")
		shex.write("PREFIX oplax: <https://w3id.org/OPLaX/> " + "\n")
		shex.write("\n")
		shex.write("# shape extracted from dataset " + topic_subkg + " which is derived from " + wikidata_kg + ", dated " + date_wikidata_dump[:4] + "-" + date_wikidata_dump[4:6] + "-" + date_wikidata_dump[6:])
		shex.write("\n")
		shex.write("\n")
		shex.write("start = @<" + domain_label[1:-1] + "> \n")
		shex.write("\n")
		shex.write("<" + domain_label[1:-1] + "> { wdt:P31 [wd:" + domain_class + "] ; \n")
		shex.write("\n")

	for index, row in triplets_df.iterrows():

		prop = row["property"]
		
		# check if the range is a Qid and save it in a set
		if re.match("Q([0-9]+)", row["range"]):
			Q_props.add(prop)

	for index, row in properties_df.iterrows():
		prop = row["property"]
		probability = row["percentage"]

		if prop in Q_props:
			with open(output_shex, "a") as shex:
				comment = "# " + str(domain_label) + " " + str(row["property;label"]) + " 'entity'" + "\n"
				final_comment = comment.replace("@en", "")
				shex.write(final_comment)

				shex.write("wdt:" + prop + " { wdt:P31 [wd:Q35120] } ;" + "   # probability of constraint: " + probability + " \n" + "\n")

	datatype_ranges = set()

	for index, row in triplets_df.iterrows():

		prop = row["property"]
		
		# check if the range is a Qid
		if re.match("Q([0-9]+)", row["range"]):
			range_class = "wd:" + row["range"]
		
		# else the range is a datatype
		else:
			if row["range"] == "external-id":
				range_class = "xsd:string"
			elif row["range"] == "string":
				range_class = "xsd:string"
			elif row["range"] == "commonsMedia":
				range_class = "xsd:string"
			elif row["range"] == "url":
				range_class = "xsd:string"
			elif row["range"] == "monolingualtext":
				range_class = "rdf:langString"
			elif row["range"] == "globecoordinate":
				range_class = "geo:wktLiteral"
			elif row["range"] == "time":
				range_class = "xsd:dateTime"
			elif row["range"] == "quantity":
				range_class = "xsd:decimal"		
			else:
				range_class = "wikibase:" + row["range"].capitalize()
				datatype_ranges.add(range_class)
		
		probability = row["percentage"]

		with open(output_shex, "a") as shex:
			if re.match("Q([0-9]+)", row["range"]):
				comment = "# " + str(row["domain;label"]) + " " + str(row["property;label"]) + " " + str(row["range;label"]) + "\n"
				final_comment = comment.replace("@en", "")
				shex.write(final_comment)

				shex.write("wdt:" + prop + " { wdt:P31 [" + range_class + "] } ;   # probability of constraint: " + probability + " \n" + "\n")
			else:
				comment = "# " + str(row["domain;label"]) + " " + str(row["property;label"]) + " " + str(row["range"]) + "\n"
				final_comment = comment.replace("@en", "")
				shex.write(final_comment)

				shex.write("wdt:" + prop + " " + range_class + " ;   # probability of constraint: " + probability + " \n" + "\n")		
			
			

	with open(output_shex, "a") as shex:
		shex.write("\n }")

if __name__ == '__main__':
	parser = argparse.ArgumentParser()

	# Parameters
	parser.add_argument('--properties_input_tsv', type=str, required=True)
	parser.add_argument('--triplets_input_tsv', type=str, required=True)
	parser.add_argument('--output_folder', type=str, required=True)
	parser.add_argument('--topic', type=str, required=True)
	parser.add_argument('--date_wikidata_dump', type=str, required=True)
	parser.add_argument('--thresholds', type=str, required=True)


	args = parser.parse_args()
    
	triplets_to_shapes(args.properties_input_tsv, args.triplets_input_tsv, args.output_folder, args.topic, args.date_wikidata_dump, args.thresholds)
