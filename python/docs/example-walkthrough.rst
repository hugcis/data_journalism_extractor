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
  where the root ``publications`` has been removed to keep the array. It was
  further inserted in a Mongo database with ``mongoimport --jsonArray --db $DB_NAME 
  --collection publications --file hatvpmongo.json``

* ``wiki.csv`` is the result of retreiving the Wikipedia pages of all MPs and
  splitting those into sentences to write in a CSV file ``$NAME,$SENTENCE``
  for each MP. 

* A Postgres database dump is also available. It contains a corpus of tweets of
  MPs and lobbyists along with the accounts that retweeted them. The whole database
  dump is available to download from this `Google Drive
  link <https://drive.google.com/file/d/1CAbx7HHsMVGXH8MTm3CGnFWXtU3SzcHQ/view?usp=sharing>`_.
  It is a tar archive that you can uncompress with ``tar -xvf twitter.dump.bz2``


Anatomy of the program
----------------------

Tweets
^^^^^^

The tweets are organised in three tables. 

* The ``user`` table contains the primary key ``uid`` (the Twitter id),
  and the ``screen_name`` of a user.

* The ``checked_statuses`` table that represents single tweets. It contains a 
  ``sid``, a ``uid`` referencing a user a ``text`` and a boolean ``ret_checked``
  indicating wethter retweeters have been fetched from the Twitter API for this 
  status (This is not always the case because of the limits of the API that
  make fetching tweets a lot faster than fetching retweeters)

* The ``retweeted_statuses`` table that represents the action of retweeting a tweet. 
  They have an ID ``rid``, a user ID ``uid`` and a status ID ``sid``. 

The twitter accounts of both the MPs and lobbyists come from their respective data export
``deputes.csv`` under the column ``twitter`` and the ``lienPageTwitter`` field in 
MongoDB documents representing the lobbyists. 