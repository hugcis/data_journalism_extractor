# Data Journalism Extractor

This project is an attempt to create a tool to help journalists extract and process
data at scale, from multiple **heterogenous data sources** while leveraging
powerful and complex **database**, **information extraction** and **NLP** tools with
**limited programming knowledge**.

## Features

This software is based on `Apache Flink <https://flink.apache.org/>`_, a stream processing
framework similar to Spark written in Java and Scala.
It executes dataflow programs, is highly scalable and integrates easily with other Big Data
frameworks and tools such as [Kafka](https://kafka.apache.org/), [HDFS](https://hadoop.apache.org/),
[YARN](https://hadoop.apache.org/docs/current/hadoop-yarn/hadoop-yarn-site/YARN.html),
[Cassandra](https://cassandra.apache.org/) or [ElasticSearch](https://www.elastic.co/).

Although you can work with custom dataflow programs that suits your specific needs,
one doesn't need to know programming, Flink or Scala to work with this tool and build complex
dataflow programs to achieve some of the following operations:

* Extract data from **relational databases** (Postgres, MySQL, Oracle), **NoSQL** databases
  (MongoDB), CSV files, HDFS, etc.
* Use complex processing tools such as **soft string-matching functions**, **link extractions**, etc.
* Store outputs in multiple different data sinks (CSV files, databases, HDFS, etc.)

## Documentation

Documentation about the project is available at this
[link](https://data-journalism-extractor.readthedocs.io/en/latest/).

## Run an example

The generated code is a Flink application project using Scala and SBT.

To run and test your application locally, you can just execute `sbt run` then select the main class
that contains the Flink job.

You can also package the application into a fat jar with `sbt assembly`, then submit it as usual, with something like:

```[bash]
flink run -c core.ScalaTempTest scala/target/scala-2.11/test-assembly-0.1-SNAPSHOT.jar
```

You can also run your application from within IntelliJ:  select the classpath of the 'mainRunner' module in the run/debug configurations.
Simply open 'Run -> Edit configurations...' and then select 'mainRunner' from the "Use classpath of module" dropbox.

## Run the tests

### Python tests

The python tests can easily be run with the command `make test` in the parent directory.

All the python tests are in `$ROOT/python/tests`.
