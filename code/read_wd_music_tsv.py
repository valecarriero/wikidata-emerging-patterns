import pandas as pd
import sys

# i read a tsv file, with a subject column, an object column and a predicate column
# i return a list with both subjects and objects, and a list with the predicates (unique values)
def read_wd_music_facts(file):
	tsv = pd.read_csv(file, delimiter="\t")


	#for i, row in tsv.iterrows():
	subjects = list(tsv["subject"].unique())
	objects = list(tsv["object"].unique())
	predicates = list(tsv["predicate"].unique())


	for n, i in enumerate(subjects):
		#subjects[n] = "https://www.wikidata.org/entity/" + i
		subjects[n] = "wd:" + i
	for n, i in enumerate(objects):
		objects[n] = "wd:" + i
	for n, i in enumerate(predicates):
		predicates[n] = "wd:" + i

	subjects_objects = list(set(subjects + objects))


	return subjects_objects, predicates
	

if __name__ == '__main__':
	read_wd_music_facts(sys.argv[1])