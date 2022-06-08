import sys
from rdflib import *
from rdflib.plugins.sparql import *
from SPARQLWrapper import SPARQLWrapper, RDFXML
from string import Template



def rdf_graph_wd_music(subjectobjects_list, predicates_list):
	wd_music_rdf_graph = Graph()

	sparql = SPARQLWrapper("https://query.wikidata.org/sparql")

	query_class_domain = Template("""

    CONSTRUCT {?prop rdfs:domain ?class . ?prop rdfs:label ?propertylabel . ?class rdfs:label ?classlabel} 
    WHERE {$instance wdt:P31 ?class . ?prop p:P2302 ?o . ?o ps:P2302 wd:Q21503250 ; pq:P2308 ?class . 
		OPTIONAL{?class rdfs:label ?classlabel FILTER (lang(?classlabel)="en")} 
		OPTIONAL{?prop rdfs:label ?propertylabel FILTER (lang(?propertylabel)="en")} }
	""")

	query_class_range = Template("""

    CONSTRUCT {?prop rdfs:range ?class . ?prop rdfs:label ?propertylabel . ?class rdfs:label ?classlabel} 
    WHERE {$instance wdt:P31 ?class . ?prop p:P2302 ?o . ?o ps:P2302 wd:Q21510865 ; pq:P2308 ?class . 
		OPTIONAL{?class rdfs:label ?classlabel FILTER (lang(?classlabel)="en")} 
		OPTIONAL{?prop rdfs:label ?propertylabel FILTER (lang(?propertylabel)="en")} }

	""")

	query_inverse_properties = Template("""

    CONSTRUCT {$prop owl:inverseOf ?inverseprop . ?inverseprop rdfs:range ?inverserange . ?inverseprop rdfs:domain ?inversedomain . ?inverseprop rdfs:label ?inversepropertylabel .} 
    WHERE {
      {$prop wdt:P1696 ?inverseprop . ?inverseprop p:P2302 ?o . ?o ps:P2302 wd:Q21510865 ; pq:P2308 ?inverserange .
      OPTIONAL{?inverseprop rdfs:label ?inversepropertylabel FILTER (lang(?inversepropertylabel)="en")} }
      UNION
      {$prop wdt:P1696 ?inverseprop . ?inverseprop p:P2302 ?o . ?o ps:P2302 wd:Q21503250 ; pq:P2308 ?inversedomain .
      OPTIONAL{?inverseprop rdfs:label ?inversepropertylabel FILTER (lang(?inversepropertylabel)="en")} } 
      }
	""")

	query_property_domain = Template("""
	CONSTRUCT {$prop rdfs:domain ?domain . $prop rdfs:label ?propertylabel . ?domain rdfs:label ?domainlabel} 
	WHERE {
	$prop p:P2302 ?o . ?o ps:P2302 wd:Q21503250 ; pq:P2308 ?domain . 
	OPTIONAL{$prop rdfs:label ?propertylabel FILTER (lang(?propertylabel)="en")}
	OPTIONAL{?domain rdfs:label ?domainlabel FILTER (lang(?domainlabel)="en")}
	}
	""" )

	query_property_range = Template("""
	CONSTRUCT {$prop rdfs:range ?range . $prop rdfs:label ?propertylabel . ?range rdfs:label ?rangelabel} 
	WHERE {
	$prop p:P2302 ?o . ?o ps:P2302 wd:Q21510865 ; pq:P2308 ?range . 
	OPTIONAL{$prop rdfs:label ?propertylabel FILTER (lang(?propertylabel)="en")}
	OPTIONAL{?range rdfs:label ?rangelabel FILTER (lang(?rangelabel)="en")} }
	""" )

	for subjobj in subjectobjects_list:
		#domains
		sparql.setQuery(query_class_domain.substitute(instance=subjobj))

		sparql.setReturnFormat(RDFXML)
		sparql_results = sparql.query().convert()

		wd_music_rdf_graph += sparql_results

		#ranges
		sparql.setQuery(query_class_range.substitute(instance=subjobj))

		sparql.setReturnFormat(RDFXML)
		sparql_results = sparql.query().convert()

		wd_music_rdf_graph += sparql_results

	# for subjobj in subjectobjects_list:
	# 	sparql.setQuery(query_class_range.substitute(instance=subjobj))

	# 	sparql.setReturnFormat(RDFXML)
	# 	sparql_results = sparql.query().convert()

	# 	wd_music_rdf_graph += sparql_results

	for pred in predicates_list:
		#domains
		sparql.setQuery(query_property_domain.substitute(prop=pred))
		sparql.setReturnFormat(RDFXML)
		sparql_results = sparql.query().convert()

		wd_music_rdf_graph += sparql_results

		#ranges
		sparql.setQuery(query_property_range.substitute(prop=pred))
		sparql.setReturnFormat(RDFXML)
		sparql_results = sparql.query().convert()

		wd_music_rdf_graph += sparql_results

		#inverseproperties
		sparql.setQuery(query_inverse_properties.substitute(prop=pred))
		sparql.setReturnFormat(RDFXML)
		sparql_results = sparql.query().convert()

		wd_music_rdf_graph += sparql_results
	
	count = 0
	for s, p, o in wd_music_rdf_graph:
		count += 1		
		print(s, p, o)
	print(count)

rdf_graph_wd_music(["wd:Q192185"], [])

