package core

import core.reader.JsonReader
import org.apache.flink.api.scala._
import org.apache.flink.core.fs.FileSystem
import org.apache.flink.util.Collector
import org.apache.flink.api.common.functions.{FlatMapFunction, MapFunction}
import edu.stanford.nlp.simple.Sentence

import scala.collection.JavaConverters._


object ScalaTempTest {

  def main(args: Array[String]) {

    // set up the execution environment
    val env = ExecutionEnvironment.getExecutionEnvironment
    
    
    
    // ===== CSV Importer module extractor1 =====
    
    val filePath_extractor1 = "/Users/hugo/Work/limsi-inria/tests/test/deputes.csv"
    val lineDelimiter_extractor1 = "\n"
    val fieldDelimiter_extractor1 = ";"
    
    val extractor1 = env.readCsvFile[(String,String)](filePath_extractor1, lineDelimiter_extractor1, fieldDelimiter_extractor1)
    
    // ===== CSV Importer module extractor4 =====
    
    val filePath_extractor4 = "/Users/hugo/Work/limsi-inria/tests/test/wiki.csv"
    val lineDelimiter_extractor4 = "\n"
    val fieldDelimiter_extractor4 = "|"
    val quoteCharacter_extractor4 = '$'
    val extractor4 = env.readCsvFile[(String,String)](filePath_extractor4, lineDelimiter_extractor4, fieldDelimiter_extractor4, quoteCharacter_extractor4)
    
    // ===== JSON Importer module extractor2 =====
    
    val filePath_extractor2 = "/Users/hugo/Work/limsi-inria/tests/test/hatvp.json"
    val mainField_extractor2 = "publications"
    val requiredFields_extractor2 = Array("denomination","identifiantNational")
    val extractor2 = JsonReader[(String,String)](env, filePath_extractor2, mainField_extractor2, requiredFields_extractor2).getInput
    
    // ===== Entity extractor linking1 =====
    
    val linking1 = extractor4.cross(extractor2).flatMap(new extract_extractor4_extractor2)
    
    // ===== Projection projection1 =====
    
    val projection1 = linking1.map { set => (set._1, set._3)}.distinct()
    
    // ===== CSV Output File output1 =====
    
    val filePath_output1 = "/Users/hugo/Work/limsi-inria/tests/test/output.csv"
    projection1.writeAsCsv(filePath_output1, writeMode=FileSystem.WriteMode.OVERWRITE)

    // ===== Execution =====
    var sent = new Document("Dominic is there!")
    projection1.map(new mapsimple).print()
    // env.execute()
  }

  
  
  // ===== Entity extractor FlatMapFunction linking1=====
  
  private class extract_extractor4_extractor2 extends FlatMapFunction[((String,String), (String,String)), (String,String,String)] {
      override def flatMap(value: ((String,String), (String,String)), out: Collector[(String,String,String)]): Unit = {
        val d = (raw"\b(" + value._2._1.toLowerCase + raw")\b").r
        if (d.findFirstIn(value._1._2.toLowerCase).nonEmpty) out.collect((value._1._1, value._1._2, value._2._1))
      }
  }


  private class mapsimple extends MapFunction[(String, String), (String, String)] {

    override def map(value: (String, String)): (String, String) = {

      //var sent: Sentence = new Sentence("lucy in the sky")
      //println(sent.nerTags())

      //val tags = sent.nerTags()
      (value._1, "dom")
    }
  }
}