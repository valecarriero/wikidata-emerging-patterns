# Results on the portion of Wikidata addressing the art, architecture and archaeology (AAA) domain

## Input
The files that have been given as input for performing these experiments can be found in [this folder](https://drive.google.com/drive/folders/1l5Suqku_KFfxgAG5q5cNqpsJTvMoQqsm?usp=sharing).

## Output

The `classes.tsv` file contains all the classes that have instances in the input subgraph on AAA, with their number of instances and frequentist probability (# instances of the class / total # instances).

The `classes_95_11.tsv` file contains the 11 classes that have been selected based on the 0.95 threshold, with their number of instances and frequentist probability.

The folder `all_subgraphs` contains all the subgraphs, one for each pattern, by selecting from the whole subgraph only the triples with an instance of the given class as subject.  E.g., for the class _album_, we will build a subgraph containing all the triples about instances of album.

The folder `patterns` contains the actual results of the patterns extraction method applied to the AAA Wikidata subgraph. There is one subfolder for each pattern. In each subfolder, the relevant files are the following:
- the file `[CLASS]-properties.tsv` contains the list of properties involved in at least one triple, with the number of distinct instances that are subject of at least one triple involving that property and the frequentist probability
- the file `[CLASS]-properties_85_[NUMBER-OF-PROPERTIES].tsv` contains the properties that have been selected for that pattern based on the 0.85 threshold, with their number of occurrences and the frequentist probability
- the file `[CLASS]-dr-pairs-frequent-properties_85.tsv` contains all the triplets (<domain, property, range>) involving the most frequent properties and instantiated in the subgraph, with their number of occurrences and the frequentist probability
- the file `[CLASS]-dr-pairs-frequent-properties_85_50_[NUMBER-OF-TRIPLETS].tsv` contains the triplets that have been selected based on the 0.50 threshold, with their number of occurrences and the frequentist probability
- the file `[CLASS]_probabilistic_pattern.ttls` contains the pattern expressed in rdf-star, using owl-star
- the file `[CLASS]_shape.shex` contains the pattern expressed as a ShEx shape

Here's an example of a pattern extracted from the Wikidata subgraph on AAA, corresponding to the `Q482994/Q482994-dr-pairs-frequent-properties_85_50_18.tsv`, `Q482994/Q482994_probabilistic_pattern.ttls`, and `Q482994/Q482994_shape.shex` files 

<img width="646" alt="Screenshot 2023-01-02 at 15 52 29" src="https://user-images.githubusercontent.com/36740200/216062969-e8dd0ac6-a6bf-4fae-bdad-23dfcca3965c.png">

