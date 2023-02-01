# Wikidata Emerging Patterns
This repository contains the code for extracting empirical ontology design patterns that emerge from (a subgraph of) Wikidata, and the results of the experiments focusing on a subgraph about the music domain and a subgraph on the art, architecture and archaeology domain.

These patterns are expressed in the form of `< domain, property, range >` triplets, where `domain` is the type (`wdt:P31`) of the subject and `range` is either the type of the object (when the object is a `wikibase-item`) or the wikidata `data type`.

Each triplet is associated with the number of instances in the Wikidata (sub-)KG that comply with that triplet, i.e. it is associated with its occurrences, and its frequentist probability, i.e. the ratio between the number of instances that are subject of at least one triple with that property and range, and the total number of instances.

These sets of triplets are then translated into OWL existential axiom, that are part of an OWL ontology design pattern.
Each axiom is annotated with its frequentist probability with respect to the specific pattern.
The patterns are expressed using [rdf-star](https://w3c.github.io/rdf-star/cg-spec/editors_draft.html) and relying on the [owl-star](https://github.com/cmungall/owlstar/blob/master/owlstar.ttl) vocabulary. 
Additionally, each set of triplets is transformed into a shape, associating each constraint with its probability value through comments. Shapes are expressed in [ShEx](https://shex.io/).

For instance, the most frequent property of the _album_ pattern (emerging from the Wikidata portion addressing the music domain) is `wdt:performer`, and the most frequent triplet including this property is 

```
< wd:Q482994,  wdt:P175, wd:Q5 > (< album, perfomer, human >)
```
with 28,193 occurrences (out of a total of 63,213 instances of album),

while the second most frequent triplet including this property is
```
< wd:Q482994,  wdt:P175, wd:Q215380 > (< album, perfomer, musical group >)
```
with 25,521 occurrences (out of a total of 63,213 instances of album).

Here's the album pattern extracted from the Wikidata subgraph on music, using specific thresholds (0.85 for properties, 0.5 for ranges).


<img width="588" alt="Screenshot 2023-01-29 at 22 07 27" src="https://user-images.githubusercontent.com/36740200/216059563-c0eecafd-fb83-4bd1-be60-36edb7d61d98.png">




