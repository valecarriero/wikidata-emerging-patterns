import pandas as pd

def compute_ratio_indirect_direct_instances(input_indirect, input_direct, output_folder):
	indirect_df = pd.read_csv(input_indirect, sep='\t', header=0)
	direct_df = pd.read_csv(input_direct, sep='\t', header=0)

	ratio_df = pd.DataFrame({'class': [], 'ratio': [], 'class;label': []})

	classes = list(set(direct_df['class'].to_list()))

	for clas in classes:

		try:
			indirect_count = indirect_df.loc[indirect_df['class'] == clas, 'count'].iloc[0]
			direct_count = direct_df.loc[direct_df['class'] == clas, 'count'].iloc[0]

			label = indirect_df.loc[indirect_df['class'] == clas, 'class;label'].iloc[0]

			number = direct_count / indirect_count
			percentage = "{:.2%}".format(number)

			ratio_df = ratio_df.append({'class':clas, 'ratio':percentage, 'class;label':label}, ignore_index=True)
		
		except:
			continue

	initial_ratio_df = ratio_df['ratio'].str.strip('%').astype(float)
	sorted_ratio_df = ratio_df.iloc[initial_ratio_df.argsort()[::-1]]

	sorted_ratio_df.reset_index(drop=True).to_csv(output_folder + "direct_indirect_instances.tsv", sep="\t")



compute_ratio_indirect_direct_instances("/Users/vale/Documents/PhD/Music_WIKIDATA/wikidata-20220404/output/superclasses.tsv", "/Users/vale/Documents/PhD/Music_WIKIDATA/wikidata-20220404/output/classes.tsv", "/Users/vale/Documents/PhD/Music_WIKIDATA/wikidata-20220404/output/")
