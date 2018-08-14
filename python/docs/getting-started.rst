Getting started
===============

Installation
------------

Get the project from GitHub
^^^^^^^^^^^^^^^^^^^^^^^^^^^

The project can be downloaded from the GitHub repository with the command

``git clone git@github.com:hugcis/data_journalism_extractor.git your/path/``

then run ``cd your/path/`` to get started.

Dependencies
------------

The project makes use of the Apache Flink stream and batch processing framework.
Flink needs a working **Java 8.x** installation to run and is compatible with Windows,
Linux and MacOS. The code is compatible with **Flink 1.5 and above**.

Apache Flink can be installed by downloading and extracting a binary from `here <https://flink.apache.org/downloads.html>`_.

Or you can install it with a package manager of your choice (e.g. Homebrew on MacOS), 
a more detailed description `there <https://ci.apache.org/projects/flink/flink-docs-release-1.6/quickstart/setup_quickstart.html>`_.

In order to run the code, **Scala 2.12.x** and **sbt** should also be installed 
(`details <https://www.scala-sbt.org/download.html>`_).

Finally, the compiler is compatible with Python3.6 and above. You can install the 
dependencies with ``pip install -r requirements.txt`` from the main directory.

------------ 

The data journalism extractor has several modules that are based on different softwares. The 
MongoDB Importer module needs a working MongoDB installation in order to work.

To run the example one will need working Postgres and MongoDB installations.