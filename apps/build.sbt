ThisBuild / version := "0.2.0"

ThisBuild / scalaVersion := "2.12.10"

lazy val root = (project in file("."))
  .settings(
    name := "Kafka Streaming Project"
  )

libraryDependencies ++= Seq(
  "org.apache.spark" %% "spark-core" % "3.0.3",
  "org.apache.spark" %% "spark-streaming" % "3.0.2" % "provided",
  "org.apache.spark" %% "spark-streaming-kafka-0-10" % "3.0.2",
  "org.apache.spark" %% "spark-sql" % "3.0.3",
  "org.apache.kafka" % "kafka-clients" % "3.1.0",
  "org.apache.kafka" %% "kafka" % "3.1.0",
  "com.github.nscala-time" %% "nscala-time" % "2.30.0"
)

assembly / assemblyMergeStrategy := {
  case PathList("META-INF", xs @ _*) => MergeStrategy.discard
  case x => MergeStrategy.first
}