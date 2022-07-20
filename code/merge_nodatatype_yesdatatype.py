import os, glob
import pandas as pd
import argparse

# the two tsv don't have the same structure bc the datatype one doesn't have the range;label column

def merge_noyes_datatype(nodp_tsv, yesdp_tsv, output_merged_tsv):
	files = []
	files.append(nodp_tsv)
	files.append(yesdp_tsv)

	all_df = []

	for f in files:
		df = pd.read_csv(f, sep="\t")
		all_df.append(df)

	merged_df = pd.concat(all_df, ignore_index=True).fillna("-")
	merged_df.sort_values(by=['property', 'count'], ascending=[False, False])

	print(merged_df)
	merged_df.to_csv(output_merged_tsv, sep='\t', index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    # Parameters
    parser.add_argument('--nodp_tsv', type=str, required=True)
    parser.add_argument('--yesdp_tsv', type=str, required=True)
    parser.add_argument('--output_file', type=str, required=True)

    args = parser.parse_args()

    merge_noyes_datatype(args.nodp_tsv, args.yesdp_tsv, args.output_file)
