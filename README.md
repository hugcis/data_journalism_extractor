# Data Journalism Extractor

This is a proposition of an architecture for information extraction in data journalism. A high level language written
in JSON compiles to Scala code that can run a Flink based application for data processing. 

## Run an example

The generated code is a Flink application project using Scala and SBT.

To run and test your application locally, you can just execute `sbt run` then select the main class that contains the Flink job .

You can also package the application into a fat jar with `sbt assembly`, then submit it as usual, with something like: 

```[bash]
flink run -c core.ScalaTempTest scala/target/scala-2.11/test-assembly-0.1-SNAPSHOT.jar
```


You can also run your application from within IntelliJ:  select the classpath of the 'mainRunner' module in the run/debug configurations.
Simply open 'Run -> Edit configurations...' and then select 'mainRunner' from the "Use classpath of module" dropbox.
