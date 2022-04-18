name := "Kafka Streaming Project"

version := "1.0"

scalaVersion := "2.12.10"

libraryDependencies += "org.apache.spark" %% "spark-core" % "3.0.3"
libraryDependencies += "org.apache.spark" %% "spark-streaming" % "3.0.2"
libraryDependencies += "org.apache.spark" %% "spark-streaming-kafka-0-10" % "3.2.1"
libraryDependencies += "org.apache.kafka" % "kafka-clients" % "0.8.2.0"
