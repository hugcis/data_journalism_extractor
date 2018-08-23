.. data_journalism_extractor documentation master file, created by
   sphinx-quickstart on Mon Aug 13 09:58:04 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Data Journalism Extractor's documentation!
=====================================================

This project is an attempt to create a tool to help journalists extract and process
data at scale, from multiple **heterogenous data sources** while leveraging
powerful and complex **database**, **information extraction** and **NLP** tools with
**limited programming knowledge**.

Features
--------

This software is based on `Apache Flink <https://flink.apache.org/>`_, a stream processing
framework similar to Spark written in Java and Scala.
It executes dataflow programs, is highly scalable and integrates easily with other Big Data 
frameworks and tools such as `Kafka <https://kafka.apache.org/>`_, `HDFS <https://hadoop.apache.org/>`_,
`YARN <https://hadoop.apache.org/docs/current/hadoop-yarn/hadoop-yarn-site/YARN.html>`_,
`Cassandra <https://cassandra.apache.org/>`_ or `ElasticSearch <https://www.elastic.co/>`_. 

Although you can work with custom dataflow programs that suits your specific needs,
one doesn't need to know programming, Flink or Scala to work with this tool and build complex
dataflow programs to achieve some of the following operations:

  * Extract data from **relational databases** (Postgres, MySQL, Oracle), **NoSQL** databases 
    (MongoDB), CSV files, HDFS, etc.
  * Use complex processing tools such as **soft string-matching functions**, **link extractions**, etc.
  * Store outputs in multiple different data sinks (CSV files, databases, HDFS, etc.)

Some examples are in :doc:`getting-started` and :doc:`example-walkthrough`. Description of the modules
and how to use them is in :doc:`modules`.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   getting-started
   example-walkthrough
   modules


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
