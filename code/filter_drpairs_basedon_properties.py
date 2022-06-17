import numpy as np
import pandas as pd
import argparse

def filter_drpairs_basedon_properties(dr_pairs_tsv, filtered_properties_tsv, output_folder):
	properties_df = pd.read_csv(filtered_properties_tsv, delimiter="\t")
	properties_list = properties_df['property'].to_list()

	dr_pairs_df = pd.read_csv(dr_pairs_tsv, delimiter="\t")

	dr_final_df = pd.DataFrame({'domain': [], 'property': [], 'range': [], 'count': [], 'domain;label': [], 'property;label': [], 'range;label': []})

	for index, row in dr_pairs_df.iterrows():
		for prop in properties_list:
			if row['property'] == prop:
				dr_final_df = dr_final_df.append({'domain':row['domain'], 'property':row['property'], 'range':row['range'], 'count':int(row['count']), 'domain;label':row['domain;label'], 'property;label':row['property;label'], 'range;label':row['range;label']}, ignore_index=True)

	output_file = output_folder + "-dr-pairs-frequent-properties_" + filtered_properties_tsv.split("_")[-2] + ".tsv"

	dr_final_df.sort_values(["property", "count"], ascending=False).reset_index(drop=True).to_csv(output_file, sep="\t", index=False)

	print(output_file)
	return dr_final_df


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    # Parameters
    parser.add_argument('--dr_pairs', type=str, required=True)
    parser.add_argument('--filtered_properties', type=str, required=True)
    parser.add_argument('--output_folder', type=str, required=True)

    args = parser.parse_args()

    filter_drpairs_basedon_properties(args.dr_pairs, args.filtered_properties, args.output_folder)

