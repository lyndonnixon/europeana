__author__ = 'Lyndon Nixon, MODUL University'

import httplib
import json
import urllib
import urllib2 as web

from xml.dom.minidom import parse
import xml.dom.minidom

import re

# configuration

Europeana_API = 'www.europeana.eu'

#TO RUN YOU NEED THE KEYS FOR EUROPEANA API, SYNONYMS AND TRANSLATION SERVICE. 

language = 'en'
language2 = 'nl'

collection = 'COUNTRY:netherlands'
query = []

# get values of the art object characteristics

## TBD: knowing an art object in the curated data, directly extract from Editor Tool
# Only try if there is at least one value!

CHO_type = 'http://dbpedia.org/resource/Vase'
CHO_material = 'http://dbpedia.org/resource/Porcelain'
CHO_creator = ''
CHO_location = ''
CHO_year_begin = ''
CHO_year_end = ''
#CHO_date = '' This is a period made up of begin date to end date.
## TBD: if ET would use LOD URIs for time periods we would need functioning means to extract period begin and end, like this:
#CHO_year_begin = '1901'
#CHO_year_end = '2000'

def make_type_query(query,CHO_property):
    "Construct the query for types"

## get RDF/XML

    req = web.Request(CHO_property)
    req.add_header('Accept', 'application/rdf+xml')
    resp = web.urlopen(req)

    dataDOM = xml.dom.minidom.parse(resp)
    elements = dataDOM.documentElement

## get string label

    #for label in elements.getElementsByTagNameNS("*","label"):
    #    if label.getAttribute("xml:lang") == language:
    #        label_en = label.firstChild.nodeValue
    #    if label.getAttribute("xml:lang") == language2:
    #        label_nl = label.firstChild.nodeValue

    for label in elements.getElementsByTagNameNS("*","label"):
        label_en = label.firstChild.nodeValue

    labels_from = [label_en]
    labels_to = []

    print label_en

## get alternative labels

    for resource in elements.getElementsByTagNameNS("*","wikiPageRedirects"):
        resourceURI = resource.getAttribute("rdf:resource")
        resourceURIstring = str(resourceURI)

        if resourceURIstring == CHO_property:
            resourceParent = resource.parentNode
            resourceURI = resourceParent.getAttribute("rdf:about")
            resourceURIstring = str(resourceURI)

        resourceLabel = resourceURIstring[resourceURIstring.index("resource/") + len("/resource"):]
        resourceLabel = re.sub('_',' ',resourceLabel)
        resourceLabel = resourceLabel.split('(')[0]

        labels_from.append(resourceLabel)

    print labels_from

## get synonyms for all labels (currently only English supported)

    synonymURL = "http://thesaurus.altervista.org/thesaurus/v1?word="+urllib.quote_plus(label_en)+"&language=en_US&key="+synonymKey

    req = web.Request(synonymURL)
    req.add_header('Accept', 'application/rdf+xml')
    resp = web.urlopen(req)

    dataDOM = xml.dom.minidom.parse(resp)
    elements = dataDOM.documentElement

    for synonyms in elements.getElementsByTagName("synonyms"):
        synonymValues = synonyms.firstChild.nodeValue.split('|')
        for synonymValue in synonymValues:
            synonymValue = synonymValue.split('(')[0]
            labels_from.append(synonymValue)

    print labels_from

## get Dutch translation of all strings

    translateURL = "http://frengly.com/?src="+language+"&dest="+language2+"&email="+translateName+"&password="+translatePwd+"&outformat=xml&text="

    for label in labels_from:
        translateReq = translateURL + urllib.quote_plus(label)

        req = web.Request(translateReq)
        resp = web.urlopen(req)

        dataDOM = xml.dom.minidom.parse(resp)
        elements = dataDOM.documentElement

        for translation in elements.getElementsByTagName("translation"):
            translationWord = translation.firstChild.nodeValue
            labels_to.append(translationWord)

    print labels_to

## construct API query part

### compound terms: add apostraphes and replace space with a plus sign
### >1 terms: put +OR+ between terms and () around all

    term_list = ""

    for term in labels_to:
        if labels_to.index(term) > 0:
            term_list = term_list + "+OR+"
        if ' ' in term:
            term = '"'+term+'"'
            term.replace(" ","+")
        term_list = term_list + term

    if len(labels_to) > 1:
        term_list = "(" + term_list + ")"

    query_type = "what:" + term_list

    print query_type

    query.append(str(query_type))

def make_material_query(query,CHO_property):
    "Construct the query for types"

## get RDF/XML

    req = web.Request(CHO_property)
    req.add_header('Accept', 'application/rdf+xml')
    resp = web.urlopen(req)

    dataDOM = xml.dom.minidom.parse(resp)
    elements = dataDOM.documentElement

## get string label

    for label in elements.getElementsByTagNameNS("*","label"):
        if label.getAttribute("xml:lang") == language:
            label_en = label.firstChild.nodeValue
        if label.getAttribute("xml:lang") == language2:
            label_nl = label.firstChild.nodeValue

    labels_from = [label_en]
    labels_to = [label_nl]

## get alternative labels

    for resource in elements.getElementsByTagNameNS("*","wikiPageRedirects"):
        resourceURI = resource.getAttribute("rdf:resource")
        resourceURIstring = str(resourceURI)

        if resourceURIstring == CHO_property:
            resourceParent = resource.parentNode
            resourceURI = resourceParent.getAttribute("rdf:about")
            resourceURIstring = str(resourceURI)

        resourceLabel = resourceURIstring[resourceURIstring.index("resource/") + len("/resource"):]
        resourceLabel = re.sub('_',' ',resourceLabel)
        resourceLabel = resourceLabel.split('(')[0]

        labels_from.append(resourceLabel)

## get synonyms for all labels (currently only English supported)

    synonymURL = "http://thesaurus.altervista.org/thesaurus/v1?word="+urllib.quote_plus(label_en)+"&language=en_US&key="+synonymKey

    req = web.Request(synonymURL)
    req.add_header('Accept', 'application/rdf+xml')
    resp = web.urlopen(req)

    dataDOM = xml.dom.minidom.parse(resp)
    elements = dataDOM.documentElement

    for synonyms in elements.getElementsByTagName("synonyms"):
        synonymValues = synonyms.firstChild.nodeValue.split('|')
        for synonymValue in synonymValues:
            synonymValue = synonymValue.split('(')[0]
            labels_from.append(synonymValue)

    print labels_from

## get Dutch translation of all strings

    translateURL = "http://frengly.com/?src="+language+"&dest="+language2+"&email="+translateName+"&password="+translatePwd+"&outformat=xml&text="

    for label in labels_from:
        translateReq = translateURL + urllib.quote_plus(label)

        req = web.Request(translateReq)
        resp = web.urlopen(req)

        dataDOM = xml.dom.minidom.parse(resp)
        elements = dataDOM.documentElement

        for translation in elements.getElementsByTagName("translation"):
            translationWord = translation.firstChild.nodeValue
            labels_to.append(translationWord)


    print labels_to


## construct API query part

### compound terms: add apostraphes and replace space with a plus sign
### >1 terms: put +OR+ between terms and () around all

    term_list = ""

    for term in labels_to:
        if labels_to.index(term) > 0:
            term_list = term_list + "+OR+"
        if ' ' in term:
            term = '"'+term+'"'
            term = term.replace(" ","+")
        term_list = term_list + term

    if len(labels_to) > 1:
        term_list = "(" + term_list + ")"

#end

    query_format = "proxy_dc_format:" + term_list

    print query_format

    query.append(str(query_format))

def make_creator_query(query,CHO_property):
    "Construct the query for creators"

    labels = []

## get RDF/XML

    req = web.Request(CHO_property)
    req.add_header('Accept', 'application/rdf+xml')
    resp = web.urlopen(req)

    dataDOM = xml.dom.minidom.parse(resp)
    elements = dataDOM.documentElement

## get string label

    for label in elements.getElementsByTagNameNS("*","label"):
        if label.getAttribute("xml:lang") == language:
            label_en = label.firstChild.nodeValue
            labels.append(label_en)
        if label.getAttribute("xml:lang") == language2:
            label_nl = label.firstChild.nodeValue
            labels.append(label_nl)

## get alternative names

    for name in elements.getElementsByTagNameNS("*","name"):
        labels.append(name.firstChild.nodeValue)

## construct query

    term_set = set(labels)
    counter = 0
    term_list = ""

    print term_set

    for term in term_set:
        if counter > 0:
            term_list = term_list + "+OR+"
        if ' ' in term:
            term = '"'+term+'"'
            term = term.replace(" ","+")
        term_list = term_list + term
        counter = counter + 1

    if len(term_set) > 1:
        term_list = "(" + term_list + ")"

    query_creator = "who:" + term_list

    print query_creator

    query.append(str(query_creator))

def make_location_query(query,CHO_property):
    "construct the query for locations"

    labels = []

## get RDF/XML

    req = web.Request(CHO_property)
    req.add_header('Accept', 'application/rdf+xml')
    resp = web.urlopen(req)

    dataDOM = xml.dom.minidom.parse(resp)
    elements = dataDOM.documentElement

## get string label

    for label in elements.getElementsByTagNameNS("*","label"):
        if label.getAttribute("xml:lang") == language:
            label_en = label.firstChild.nodeValue
            labels.append(label_en)
        if label.getAttribute("xml:lang") == language2:
            label_nl = label.firstChild.nodeValue
            labels.append(label_nl)

## get alternative names

    #for name in elements.getElementsByTagNameNS("*","subdivisionName"):
    #    labels.append(name)

    #for name in elements.getElementsByTagNameNS("*","isPartOf"):
    #    labels.append(name)

## construct query

    term_set = set(labels)
    counter = 0
    term_list = ""

    print term_set

    for term in term_set:
        if counter > 0:
            term_list = term_list + "+OR+"
        if ' ' in term:
            term = '"'+term+'"'
            term = term.replace(" ","+")
        term_list = term_list + term
        counter = counter + 1

    if len(term_set) > 1:
        term_list = "(" + term_list + ")"

    query_location = "where:" + term_list

    print query_location

    query.append(str(query_location))

#START MAIN

# map TYPE to API

if not CHO_type:
    query.append(False)
else:
    make_type_query(query,CHO_type)

# map MATERIAL to API

if not CHO_material:
    query.append(False)
else:
    make_material_query(query,CHO_material)

# map CREATOR to API

if not CHO_creator:
    query.append(False)
else:
    make_creator_query(query,CHO_creator)

# map LOCATION to API

if not CHO_location:
    query.append(False)
else:
    make_location_query(query,CHO_location)

# map DATE to API

# regard this next line if we change how this variable is used (eg. replaced by single variable CHO_date
if not CHO_year_begin:
    query.append(False)
else:
    query_date = "YEAR:["+CHO_year_begin+"+TO+"+CHO_year_end+"]"
    query.append(query_date)

# generate API queries

# -> only construct the queries that we actually can

def make_query (newquery, counter):
    "constructs a partial query on the Europeana API and adds results to results_list"
    query_string = wskey
    firstquery = True

    for a_query in newquery:
        if a_query == False:
            pass
        elif firstquery == True:
            query_string = query_string + "&query=" + a_query
            firstquery = False
        else:
            query_string = query_string + "&qf=" + a_query

    print query_string

    conn = httplib.HTTPConnection(Europeana_API)
    API_call = "/api/v2/search.json?" + query_string
    conn.request("GET", API_call)
    response = conn.getresponse()
    my_response = response.read()
    conn.close()

    results = json.loads(my_response)

    results_total =  results['itemsCount']
    print results_total

    if results_total > 0:
        index = 0
        for i in results['items']:
            print results['items'][index]['link']
            index += 1

    counter +=  results_total
    return counter

# check we have enough values to create a valid query worth sending

print query
truequery = sum(bool(x) for x in query)
# -> at least 2 values!
if truequery < 2:
    print "I have to stop here"

results_list = []
counter = 0

wskey = "wskey=" + API_key
firstquery = True

query_string = wskey

for a_query in query:
    if a_query == False:
        pass
    elif firstquery == True:
        query_string = query_string + "&query="
        query_string = query_string + a_query
        firstquery = False
    else:
        query_string = query_string + "&qf="
        query_string = query_string + a_query

# query

print query_string

conn = httplib.HTTPConnection(Europeana_API)

API_call = "/api/v2/search.json?" + query_string

conn.request("GET", API_call)
response = conn.getresponse()
my_response = response.read()
conn.close()

results = json.loads(my_response)

# ranked list of CHO results

results_total = results['itemsCount']

if results_total > 0:
        for i in results['items']:
            print results['items'][i]['link']

#for i in results['items'][i]['id']:
#    print (i, results['items'][i]['id'])

counter +=  results_total

#add results from json into results_list
#if results_count is still under 10 (or something) try next query

newquery = query[0:4]
if counter < 11:
    counter = make_query(newquery, counter)

#next query
newquery = query[0:3]+[query[4]]
if counter < 11:
    counter = make_query(newquery, counter)

#next query
newquery = [query[0]]+query[2:]
if counter < 11:
    counter = make_query(newquery, counter)

#next query
newquery = query[0:2]+query[3:]
if counter < 11:
    counter = make_query(newquery, counter)

#next query
newquery = [query[0]]+query[2:]
if counter < 11:
    counter = make_query(newquery, counter)

#next query
newquery = query[1:]
if counter < 11:
    counter = make_query(newquery, counter)

#next query
newquery = query[0:3]
if counter < 11:
    counter = make_query(newquery, counter)

#next query
newquery = query[0:2]+[query[3]]
if counter < 11:
    counter = make_query(newquery, counter)

#next query
newquery = query[0:2]+[query[4]]
if counter < 11:
    counter = make_query(newquery, counter)

#next query
newquery = [query[0]]+query[2:4]
if counter < 11:
    counter = make_query(newquery, counter)

#next query
newquery = [query[0]]+[query[2]]+[query[4]]
if counter < 11:
    counter = make_query(newquery, counter)

#next query
newquery = [query[0]]+query[3:]
if counter < 11:
    counter = make_query(newquery, counter)

#next query
newquery = query[1:4]
if counter < 11:
    counter = make_query(newquery, counter)

#next query
newquery = query[1:3]+[query[4]]
if counter < 11:
    counter = make_query(newquery, counter)

#next query
newquery = [query[1]]+query[3:]
if counter < 11:
    counter = make_query(newquery, counter)

#next query
newquery = query[2:]
if counter < 11:
    counter = make_query(newquery, counter)

#get results

## construct response with number of matches
## with each match, providing guid, title, thumbnail, rank
## write out results

