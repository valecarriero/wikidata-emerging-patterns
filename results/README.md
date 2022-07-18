# Results

The `classes.tsv` file contains all the classes that have instances in the input domain subgraph on music, with their number of instances.

The `classes_95_7.tsv` file contains the 7 classes that have been selected based on the 0.95 threshold, with their number of instances.

The folder `all_subgraphs` contains all the subgraphs, one for each pattern, by selecting from the whole domain subgraph only the triples with an instance of the given class - or one of its subclasses - as subject.  E.g., for the class _album_, we will build a subgraph containing all the triples about instances of album or subclasses of album.
