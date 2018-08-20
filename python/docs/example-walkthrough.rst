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
  where the root ``publications`` has been removed to keep the array. 
  
  It should further be inserted in a Mongo database with ``mongoimport 
  --jsonArray --db $DB_NAME --collection publications --file hatvpmongo.json``

* ``wiki.csv`` is the result of retreiving the Wikipedia pages of all MPs and
  splitting those into sentences to write in a CSV file ``$NAME,$SENTENCE``
  for each MP. 

* A Postgres database dump is also available. It contains a corpus of tweets of
  MPs and lobbyists along with the accounts that retweeted them. The whole database
  dump is available to download from this `Google Drive
  link <https://drive.google.com/file/d/1CAbx7HHsMVGXH8MTm3CGnFWXtU3SzcHQ/view?usp=sharing>`_.
  It is a tar archive that you can uncompress with ``tar -xvf twitter.dump.bz2``.

  If you have Postgres installed, you can then do ``psql twitter < twitter.dump``


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

The operations and modules needed for extracting and using data from those sources are 
the following (you can find more detailed explanation of the capacities of each module
in the :

Extraction
##########

Three extraction modules are needed for reading the Mongo database, reading the ``deputes.csv``
file and fetching data from the Postgres database.
  
  * The Mongo reader module is specified below, where ``dbName`` is the name you chose for your
    Mongo DB, and ``"publications"`` is the name of the main collection. 

    .. code-block:: javascript

       {
            "name": "mongoDBHATVP",
            "type": "mongoImporter",
            "dbName": "testdb",
            "collection": "publications",
            "requiredFields": ["lienPageTwitter", "denomination"]
       }

    Here the reader is instructed to query both the content of ``"lienPageTwitter"`` 
    and ``"denomination"`` for each element of the collection. 

  * The CSV file reader is another module and therefore also needs both a name and
    type. 
    Moreover, a ``path`` to the file and ``dataType`` must be provided. 

    Since the delimiter in the file is ``;`` instead of the standard comma, a 
    ``fieldDelimiter`` is also added. Finally, since the CSV file has named columns,
    we can use those name to select only the two that are necessary.

    .. code-block:: javascript

       {
            "name": "extractorMPs",
            "type": "csvImporter",
            "path": "~/data_journalism_extractor/example/data/deputes.csv",
            "dataType": ["String", "String"],
            "fieldDelimiter": ";",
            "namedFields": ["nom", "twitter"]
       }

  * The Database Extractor works with any relational database that has JDBC support. 
    The module is as follow:

    .. code-block:: javascript

       {
            "name": "extractordb",
            "type": "dbImporter",
            "dbUrl": "jdbc:postgresql://localhost/twitter",
            "fieldNames": ["rt_name","screen_name"],
            "dataType": ["String", "String"],
            "query": "select rt_name, screen_name from (select rt_name, uid from (select us.screen_name as rt_name, rt.sid from retweetedstatuses as rt join users as us on (rt.uid=us.uid)) as sub join checkedstatuses as ch on (sub.sid=ch.sid)) as subsub join users on (subsub.uid=users.uid);",
            "filterNull": true
       } 

    The ``dbUrl`` field corresponds to the jdbc-format endpoint used to access the 
    database. The field names and data types must also be specified. The query above
    is quite complete because it is nested and basically retreives every pair of
    (Twitter user, Retweeter).

    The ``filterNull`` flag  set to ``true`` ensures that no null values are outputed.

Processing
##########

After the three extractions above, three data flows are available to work with: 

* ``(lobbyists Twitter name, lobbyists name)``
* ``(MPs name, MPs Twitter name)``
* ``(retweeter name, tweeter name)``

First, the extracted Twitter names of the lobbyists aren't names but URLs to 
their Twitter accounts. The first step is to extract the names from the pattern 
``"https://twitter.com/twitter-name?lang=fr"``. This can easily be done by chaining 
two string splitters to separate the strings on ``"/"`` and ``"?"``. The 
corresponding modules are:

.. code-block:: javascript

    {
        "name": "splitTwitterHATVP",
        "type": "split",
        "source": "mongoDBHATVP",
        "delimiter": "/",
        "field": 0,
        "reduce": -1
    },
    {
        "name": "splitTwitterHATVP2",
        "type": "split",
        "source": "splitTwitterHATVP",
        "delimiter": "\\?",
        "field": 1,
        "reduce": 0
    }

Note: The delimiter is a regex pattern and therefore the character ``"?"`` is
represented by ``"\?"``, but the antislash must be escaped in strings hence 
``"\\?"``. Also, column indexing starts at 0 and negative indexing is supported
for -1 only (``"reduce": -1``).

Then, a series of joins transforms pairs of Twitter names and retweeter names 
into pairs of Lobbyists and MPs names. 

There are two separate flows:
   * One for the tweets authored by lobbyists and retweeted by MPs 
     (``joinExtractorDBTwitterSplit`` and ``joinDBHATVPMPs``)
   * The other for tweets authored by MPs and retweeted by lobbyists
     (``joinExtractorDBMPs`` and ``joinDB1HATVP``)

They are explained below:

.. code-block:: javascript

   {
       "name": "joinExtractorDBTwitterSplit",
       "type": "join",
       "source1": "extractordb",
       "source2": "splitTwitterHATVP2",
       "field1": 1,
       "field2": 0,
       "leftFields": [0]
   },
   {
       "name": "joinExtractorDBMPs",
       "type": "join",
       "source1": "extractordb",
       "source2": "extractorMPs",
       "field1": 1,
       "field2": 1,
       "leftFields": [0]
   },
   {
       "name": "joinDBHATVPMPs",
       "type": "join",
       "source1": "joinExtractorDBTwitterSplit",
       "source2": "extractorMPs",
       "field1": 0,
       "field2": 1,
       "leftFields": [2],
       "rightFields": [0]
   },
   {
       "name": "joinDB1HATVP",
       "type": "join",
       "source1": "joinExtractorDBMPs",
       "source2": "splitTwitterHATVP2",
       "field1": 0,
       "field2": 0,
       "leftFields": [1],
       "rightFields": [1]
   }

Join modules have two sources with names of other upstream modules; for 
each of the sources, a field on wich to perform the join, and two optional
list of fields that allow to project the output on the desired columns. 
For example column 0 on the left and all columns on the right for module
``joinExtractorDBMPs``.

Output
######

An arbitrary number of outputs can be added at any step of the process to 
log an intermediray output for debugging or store a result. 

Two CSV outputs correspond to  both MPs' retweets of lobbyists and lobbyists'
retweets of MPs.

.. code-block:: javascript

    {
        "name": "output2",
        "type": "csvOutput",
        "source": "joinDBHATVPMPs",
        "path": "/Users/hugo/Work/limsi-inria/tests/data_journalism_extractor/example/output/output_dep_retweet_hatvp.csv"
    },
    {
        "name": "output3",
        "type": "csvOutput",
        "source": "joinDB1HATVP",
        "path": "/Users/hugo/Work/limsi-inria/tests/data_journalism_extractor/example/output/output_hatvp_retweet_dep.csv"
    }


The 

Wikipedia mentions
^^^^^^^^^^^^^^^^^^

All French MPs have Wikipedia pages. They usually contain a short bio that
gives useful information such as previous occupations or major events in the MP's
political career. The Wikipedia API can be used to download the bios and sentence
splitting can be applied to obtain the file in ``example/data/wiki.csv``.

From a list of pairs of MP name and sentence, different approaches can extract
links between MPs and lobbyists. The simplest one is consists in matching every 
occurence of a lobby's name in the sentences and treating it as an indication
of the existence of a link between the two entities. It obviously yields some false
positives but nonetheless give an indication that the corresponding lobby has had
a relation with the MP. It is the example described below. 

Extraction
##########

Data in ``wiki.csv`` is already pre-processed and thus simply needs an CSV importer
module to extract the data.

The second field is quoted between ``$`` s.

.. code-block:: javascript

   {
      "name": "extractorWiki",
      "type": "csvImporter",
      "path": "/Users/hugo/Work/limsi-inria/tests/data_journalism_extractor/example/data/wiki.csv",
      "dataType": ["String", "String"],
      "quoteCharacter": "$",
      "fieldDelimiter": "|"
   }

Processing
##########

The ``extractorLink`` module implements a mention extraction algorithm to extract
mentions of a given data flow's elements into an other data flow. 

The ``sourceExtract`` and ``targetExtract`` fields correspond to the column index 
of the source and target flow. **The source is the content mention of the target will
be extracted from.**

.. code-block:: javascript

   {
      "name": "mentionExtraction",
      "type": "extractorLink",
      "source1": "extractorWiki",
      "source2": "mongoDBHATVP",
      "sourceExtract": 1,
      "targetExtract": 1
   }