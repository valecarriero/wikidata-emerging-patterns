import pandas as pd
import argparse

def return_filtered_distribution(input_file, k, output_folder):

    if "." in k:
        k = float(k)
    else:
        k = int(k)

    df = pd.read_table(input_file)

    counts = df['count']

    filtered_counts = (abs((counts - counts.max()) / counts.max()) <= k) 
    filtered_df = df[filtered_counts]

    output_file = output_folder + "/" + input_file.split("/")[-1].split(".")[0] + "_" + str(k*100).split(".")[0] + "_" + str(filtered_df.shape[0]) + ".tsv"

    filtered_df.reset_index(drop=True).to_csv(output_file, sep="\t", index=False)

    print(output_file)
    return filtered_df
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    # Parameters
    parser.add_argument('--input_file', type=str, required=True)
    parser.add_argument('--k_value', type=str, required=True)
    parser.add_argument('--output_folder', type=str, required=True)

    args = parser.parse_args()

    return_filtered_distribution(args.input_file, args.k_value, args.output_folder)

#return_filtered_distribution("/Users/vale/Documents/PhD/Music_WIKIDATA/code/output/patterns/Q5/Q5-properties.tsv", 0.8, "/Users/vale/Documents/PhD/Music_WIKIDATA/code/test/")
#return_filtered_distribution("/Users/vale/Documents/PhD/Music_WIKIDATA/code/output-kgtk-corrupt-dump/classes.tsv", 1, "/Users/vale/Documents/PhD/Music_WIKIDATA/code/test-kgtk-corrupt-dump/max_deviation/")