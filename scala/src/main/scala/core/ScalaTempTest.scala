package core

import core.reader.{JsonReader, MongoReader}
import org.apache.flink.api.scala._
import org.apache.flink.core.fs.FileSystem
import org.apache.flink.util.Collector
import org.apache.flink.api.common.functions.FlatMapFunction
import org.apache.flink.api.common.typeinfo.TypeInformation
import org.apache.flink.api.java.io.jdbc.JDBCInputFormat
import org.apache.flink.api.java.typeutils.RowTypeInfo

object ScalaTempTest {

  def main(args: Array[String]) {

    // set up the execution environment
    val env = ExecutionEnvironment.getExecutionEnvironment
    
    
    
    // ===== CSV Importer module extractor1 =====
    
    val filePath_extractor1 = "/Users/hugo/Work/limsi-inria/tests/data_journalism_extractor/example/data/deputes.csv"
    val lineDelimiter_extractor1 = "\n"
    val fieldDelimiter_extractor1 = ";"
    val includedFields_extractor1 = Array(1, 3, 30)
    val extractor1 = env.readCsvFile[(String,String,String)](filePath_extractor1, lineDelimiter_extractor1, fieldDelimiter_extractor1, ignoreFirstLine=true, includedFields=includedFields_extractor1)
    
    // ===== Projection projection_twitter =====
    
    val projection_twitter = extractor1.map { set => (set._3)}.distinct()
    
    // ===== Mongo Importer module mongo_loader =====
    
    val mongo_loader = MongoReader[(String,String)](env, "testdb", "publications", List("lienPageTwitter","denomination")).getDataSet()
    
    // ===== CSV Importer module extractor_lex =====
    
    val filePath_extractor_lex = "/Users/hugo/Work/limsi-inria/tests/data_journalism_extractor/example/data/lex.csv"
    val lineDelimiter_extractor_lex = "\n"
    val fieldDelimiter_extractor_lex = ","
    val extractor_lex = env.readCsvFile[(String,String)](filePath_extractor_lex, lineDelimiter_extractor_lex, fieldDelimiter_extractor_lex)
    
    // ===== Split split_lex =====
    
    val split_lex = extractor_lex.map { set => (set._1,set._2.toLowerCase.split("|"))}
    
    // ===== DB Importer module extractordb =====
    
    val fieldTypes_extractordb: Array[TypeInformation[_]] = Array(createTypeInformation[String],createTypeInformation[String])
    val fieldNames_extractordb = Array("rt_name","screen_name")
    
    val rowTypeInfo_extractordb = new RowTypeInfo(fieldTypes_extractordb, fieldNames_extractordb)
    val inputFormat_extractordb = JDBCInputFormat.buildJDBCInputFormat()
      .setDrivername("org.postgresql.Driver")
      .setDBUrl("jdbc:postgresql://localhost/twitter")
      .setQuery("select rt_name, screen_name from (select rt_name, uid from (select us.screen_name as rt_name, rt.sid from retweetedstatuses as rt join users as us on (rt.uid=us.uid)) as sub join checkedstatuses as ch on (sub.sid=ch.sid)) as subsub join users on (subsub.uid=users.uid);")
      .setRowTypeInfo(rowTypeInfo_extractordb)
      .finish()
    
    val extractordb = env.createInput(inputFormat_extractordb)
    
    // ===== CSV Importer module extractor4 =====
    
    val filePath_extractor4 = "/Users/hugo/Work/limsi-inria/tests/data_journalism_extractor/example/data/wiki.csv"
    val lineDelimiter_extractor4 = "\n"
    val fieldDelimiter_extractor4 = "|"
    val quoteCharacter_extractor4 = '$'
    val extractor4 = env.readCsvFile[(String,String)](filePath_extractor4, lineDelimiter_extractor4, fieldDelimiter_extractor4, quoteCharacter_extractor4)
    
    // ===== JSON Importer module extractor2 =====
    
    val filePath_extractor2 = "/Users/hugo/Work/limsi-inria/tests/data_journalism_extractor/example/data/hatvp.json"
    val mainField_extractor2 = "publications"
    val requiredFields_extractor2 = Array("denomination","identifiantNational","activites","lienPageTwitter")
    val extractor2 = JsonReader[(String,String,String,String)](env, filePath_extractor2, mainField_extractor2, requiredFields_extractor2).getInput
    
    // ===== Split split_twitter_hatvp =====
    
    val split_twitter_hatvp = extractor2.map { set => (set._1,set._2,set._3,set._4.toLowerCase.split("/"))}
    
    // ===== Word similarity extractor tryExtractorWordSim =====
    
    val tryExtractorWordSim = split_lex.cross(split_lex) {
        (c1, c2) => 
            val set1 = c1._2.toSet
            val set2 = c2._2.toSet
            val dist = set1.intersect(set2).size / set1.union(set2).size
        (c1, c2, dist)
    }
    
    // ===== Entity extractor linking1 =====
    
    val linking1 = extractor4.cross(extractor2).flatMap(new extract_extractor4_extractor2)
    
    // ===== Projection projection1 =====
    
    val projection1 = linking1.map { set => (set._1,set._3)}.distinct()
    
    // ===== CSV Output File output1 =====
    
    val filePath_output1 = "/Users/hugo/Work/limsi-inria/tests/data_journalism_extractor/example/output/output.csv"
    projection1.writeAsCsv(filePath_output1, writeMode=FileSystem.WriteMode.OVERWRITE)

    // ===== Execution =====

    env.execute()
  }

  
  
  // ===== Entity extractor FlatMapFunction linking1=====
  
  private class extract_extractor4_extractor2 extends FlatMapFunction[((String,String), (String,String,String,String)), (String,String,String)] {
      override def flatMap(value: ((String,String), (String,String,String,String)), out: Collector[(String,String,String)]): Unit = {
        val d = (raw"\b(" + value._2._1.toLowerCase + raw")\b").r
        if (d.findFirstIn(value._1._2.toLowerCase).nonEmpty) out.collect((value._1._1,value._1._2,value._2._1))
      }
  }
}