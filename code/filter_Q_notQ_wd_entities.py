import sys
import csv
import re as re
import pandas as pd

def filter_Q_notQ(input_tsv, output_Q_tsv, output_notQ_tsv):

	input_df = pd.read_csv(input_tsv, sep='\t',quoting=csv.QUOTE_NONE)

	Q_rows = []
	notQ_rows = []

	for index, row in input_df.iterrows():
		if re.match("Q([0-9]+)", row['id']):
			Q_rows.append(row['id'])
		else:
			notQ_rows.append(row['id'])

	Q_df = pd.DataFrame(Q_rows, columns =['id'])
	notQ_df = pd.DataFrame(notQ_rows, columns =['id'])

	Q_df.to_csv(output_Q_tsv, sep='\t', quoting=csv.QUOTE_NONE, index=False)
	notQ_df.to_csv(output_notQ_tsv, sep='\t',quoting=csv.QUOTE_NONE, index=False)


if __name__ == '__main__':
	filter_Q_notQ(sys.argv[1], sys.argv[2], sys.argv[3])