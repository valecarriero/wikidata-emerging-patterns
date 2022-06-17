import pandas as pd
import argparse

def return_filtered_distribution_drpairs(input_file, k, output_folder):

    drpairs_df = pd.read_table(input_file)
    drpairs_props = set(drpairs_df['property'].to_list())

    if "." in k:
        k = float(k)
    else:
        k = int(k)

    prop_drpairs_list = list()

    for prop in drpairs_props:
        prop_df = drpairs_df.loc[drpairs_df['property'] == prop]
        prop_counts = prop_df['count']

        filtered_counts = (abs((prop_counts - prop_counts.max()) / prop_counts.max()) <= k) 

        filtered_df = prop_df[filtered_counts]

        prop_drpairs_list.append(filtered_df) 


    all_df = pd.concat(prop_drpairs_list)

    output_file = output_folder + "/" + input_file.split("/")[-1].split(".")[0] + "_" + str(k*100).split(".")[0] + "_" + str(all_df.shape[0]) + ".tsv"
    

    all_df.reset_index(drop=True).to_csv(output_file, sep="\t", index=False)

    print(output_file)
    return all_df

        

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    # Parameters
    parser.add_argument('--input_file', type=str, required=True)
    parser.add_argument('--k_value', type=str, required=True)
    parser.add_argument('--output_folder', type=str, required=True)

    args = parser.parse_args()

    return_filtered_distribution_drpairs(args.input_file, args.k_value, args.output_folder)

