import pandas as pd
import re as re
import argparse

def triplets_to_axioms(properties_input_tsv, triplets_input_tsv, output_folder, topic, date_wikidata_dump, thresholds):

	properties_df = pd.read_csv(properties_input_tsv, delimiter="\t")

	triplets_df = pd.read_csv(triplets_input_tsv, delimiter="\t")
	# domain	property	range	count	domain;label	property;label	range;label

	domain_class = triplets_input_tsv.split("/")[-1].split("-")[0]

	domain_label = triplets_df["domain;label"][0].split("@")[0]

	output_ttls = output_folder + "/" + domain_class + "_probabilistic_pattern.ttls"

	Q_props = set()

	prob_pattern = "weps:" + topic + "_" + domain_class + "_" + thresholds

	topic_subkg = "weps:wikidata_" + topic + "_subkg_" + date_wikidata_dump

	wikidata_kg = "weps:wikidata_" + date_wikidata_dump


	with open(output_ttls, "a") as ttls:
		ttls.write("@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> ." + "\n")
		ttls.write("@prefix wd: <http://www.wikidata.org/entity/> ." + "\n")
		ttls.write("@prefix wdt: <http://www.wikidata.org/prop/direct/> ." + "\n")
		ttls.write("@prefix wikibase: <http://wikiba.se/ontology#> ." + "\n")
		ttls.write("@prefix dcterms: <http://purl.org/dc/terms/> ." + "\n")
		ttls.write("@prefix os: <http://w3id.org/owlstar/> ." + "\n")
		ttls.write("@prefix oplax: <https://w3id.org/OPLaX/> ." + "\n")
		ttls.write("@prefix weps: <https://w3id.org/wikidata-eps/> ." + "\n")
		ttls.write("\n")
		ttls.write(prob_pattern + " rdf:type oplax:ProbabilisticPattern ; \n dcterms:source " + topic_subkg + " ; \n dcterms:references wd:" + domain_class + " . \n")
		ttls.write("\n")
		ttls.write(topic_subkg + " rdf:type dcterms:Dataset ; \n dcterms:isPartOf " + wikidata_kg + " ; \n dcterms:subject wd:Q638 . \n")
		ttls.write("\n")
		ttls.write(wikidata_kg + " rdf:type dcterms:Dataset ; \n dcterms:hasPart " + topic_subkg + " ; \n dcterms:date \"" + date_wikidata_dump[:4] + "-" + date_wikidata_dump[4:6] + "-" + date_wikidata_dump[6:] + "\"^^xsd:date . \n")
		ttls.write("\n")


	for index, row in triplets_df.iterrows():

		prop = row["property"]
		
		# check if the range is a Qid and save it in a set
		if re.match("Q([0-9]+)", row["range"]):
			Q_props.add(prop)

	for index, row in properties_df.iterrows():
		prop = row["property"]
		probability = row["percentage"]

		if prop in Q_props:
			with open(output_ttls, "a") as ttls:
				comment = "# " + str(domain_label) + " " + str(row["property;label"]) + " 'entity'" + "\n"
				final_comment = comment.replace("@en", "")
				ttls.write(final_comment)

				ttls.write("<< << wd:" + domain_class + " wdt:" + prop + " wd:Q35120" + " >> os:interpretation os:AllSomeInterpretation . >> os:frequentistProbability \"" + probability + "\" ; oplax:isNativeTo " + prob_pattern + " ." + "\n" + "\n")


	for index, row in triplets_df.iterrows():

		prop = row["property"]
		
		# check if the range is a Qid
		if re.match("Q([0-9]+)", row["range"]):
			range_class = "wd:" + row["range"]
		
		# else the range is a datatype
		else:
			if row["range"] == "external-id":
				range_class = "\"External-ID\""
			else:
				range_class = "wikibase:" + row["range"].capitalize()
			#range_class = "\"" + row["range"] + "\""
		
		probability = row["percentage"]

		with open(output_ttls, "a") as ttls:
			if re.match("Q([0-9]+)", row["range"]):
				comment = "# " + str(row["domain;label"]) + " " + str(row["property;label"]) + " " + str(row["range;label"]) + "\n"
			else:
				comment = "# " + str(row["domain;label"]) + " " + str(row["property;label"]) + " " + str(row["range"]) + "\n"
			
			final_comment = comment.replace("@en", "")
			ttls.write(final_comment)

			ttls.write("<< << wd:" + domain_class + " wdt:" + prop + " " + range_class + " >> os:interpretation os:AllSomeInterpretation . >> os:frequentistProbability \"" + probability + "\" ; oplax:isNativeTo " + prob_pattern + " ." + "\n" + "\n")

	
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
    
	triplets_to_axioms(args.properties_input_tsv, args.triplets_input_tsv, args.output_folder, args.topic, args.date_wikidata_dump, args.thresholds)