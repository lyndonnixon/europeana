# europeana
Python script for Europeana API based on semantic annotation of CHOs

# author
Lyndon Nixon, MODUL University Vienna

# explanation
currently standalone, in that the variables are set in the script. A REST API version is planned to pass parameter values. 

since it is public, I didnt publish my API keys. These are available on request or the user creates their own. 

You can change the 2nd language (ISO 2 letter code) but keep the first always as English since we expect English DBPedia resources. 

The CHO_* variables are the art object properties annotated for our semantic model. See our paper 'LinkedCulture: browsing related Europeana objects while watching a cultural heritage TV program',
in Personalised Access to Cultural Heritage (PATCH) workshop, co-located with the International User Interfaces Conference (IUI 2015), Atlanta, USA, March 2015

At least 2 properties are needed for queries to be made. The output is just to print the "link" - JSON metadata - of every art object in the Europeana response, and it stops once more than 10 objects have been found.



