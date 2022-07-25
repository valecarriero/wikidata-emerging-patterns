# Wikidata Emerging Patterns
This repository contains the code for extracting emerging patterns from a subgraph of Wikidata and the results of the experiments focusing on a subgraph about the music domain.

These patterns are expressed in the form of `< domain, property, range >` triplets, where `domain` is the type (`wdt:P31`) of the subject and `range` is either the type of the object (when the object is a `wikibase-item`) or the wikidata `data type`.

Each triplet is associated with the number of instances in the Wikidata (sub-)KG that comply with that triplet, i.e. it is associated with its occurrences.

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


<img src="https://user-images.githubusercontent.com/36740200/179528783-239fc2de-3de1-4fb1-a5e9-a5791b25fb5b.png" width=70% height=70%>



