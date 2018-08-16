Example Walkthrough
===================

The following example will introduce several of the project's modules and 
their functioning. It was the initial motivation for building this software
and was both a source of inspiration for building modules and a testing 
dataset. 

Context
-------

The idea behind the example was to take advantage of multiple open data sets made
available by institutions, associations, or open APIs and try to identify "links"
(of influence or else) between French MPs and lobbyists. 

With the available data, three ways of identifying links came to mind:

* Tweets
* Wikipedia mentions
* Semantic field

Data
----

The data is available in the ``example/data`` directory. The list of files is:

* ``deputes.csv`` the standard CSV export of http://www.nosdeputes.fr 's data.
  (Available at https://www.nosdeputes.fr/deputes/enmandat/csv)

* ``hatvpmongo.json`` the JSON export from https://www.hatvp.fr/agora/opendata/agora_repertoire_opendata.json
  where the root ``publications`` has been removed to keep the array. It was further inserted 
  in a Mongo database with ``mongoimport --jsonArray --db $DB_NAME --collection publications --file hatvpmongo.json``

* ``wiki.csv`` is the result of retreiving the Wikipedia pages of all MPs and splitting those into sentences 
  to write in a CSV file ``$NAME,$SENTENCE`` for each MP. 

* A Postgres database dump is also available. It contains a corpus of tweets of MPs and lobbyists
  along with the accounts that retweeted them. 