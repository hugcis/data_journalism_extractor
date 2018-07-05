ThisBuild / resolvers ++= Seq(
  "Apache Development Snapshot Repository" at "https://repository.apache.org/content/repositories/snapshots/",
  Resolver.mavenLocal
)

resolvers ++= Seq(
  Resolver.sonatypeRepo("releases"),
  Resolver.sonatypeRepo("snapshots")
)

name := "test"

version := "0.1-SNAPSHOT"

organization := "core"

ThisBuild / scalaVersion := "2.11.12"

val flinkVersion = "1.5.0"

val flinkDependencies = Seq(
  "org.apache.flink" %% "flink-scala" % flinkVersion % "provided",
  "org.apache.flink" %% "flink-streaming-scala" % flinkVersion % "provided")

lazy val root = (project in file(".")).
  settings(
    libraryDependencies ++= flinkDependencies
  )

libraryDependencies ++= Seq(
  "com.chuusai" %% "shapeless" % "2.3.3",
  "org.apache.flink" %% "flink-table" % flinkVersion,
  "com.nrinaudo" %% "kantan.xpath" % "0.4.0",
  "io.argonaut" %% "argonaut" % "6.2"
)


assembly / mainClass := Some("core.ScalaTempTest")

// make run command include the provided dependencies
Compile / run  := Defaults.runTask(Compile / fullClasspath,
  Compile / run / mainClass,
  Compile / run / runner
).evaluated

// stays inside the sbt console when we press "ctrl-c" while a Flink programme executes with "run" or "runMain"
Compile / run / fork := true
Global / cancelable := true

// exclude Scala library from assembly
assembly / assemblyOption  := (assembly / assemblyOption).value.copy(includeScala = false)
