package core

import core.reader.{JsonReader, MongoReader, SQLDBReader}
import org.apache.flink.api.scala._
import org.apache.flink.core.fs.FileSystem
import org.apache.flink.util.Collector
import org.apache.flink.api.common.functions.FlatMapFunction
import org.apache.flink.api.common.typeinfo.TypeInformation
import org.apache.flink.types.Row

object ScalaTempTest {

  def main(args: Array[String]) {

    // set up the execution environment
    val env = ExecutionEnvironment.getExecutionEnvironment
    
    
    
    // ===== CSV Importer module extractor1 =====
    
    val filePath_extractor1 = "/Users/hugo/Work/limsi-inria/tests/data_journalism_extractor/example/data/deputes.csv"
    val lineDelimiter_extractor1 = "\n"
    val fieldDelimiter_extractor1 = ";"
    val includedFields_extractor1 = Array(1, 30)
    val extractor1 = env.readCsvFile[(String,String)](filePath_extractor1, lineDelimiter_extractor1, fieldDelimiter_extractor1, ignoreFirstLine=true, includedFields=includedFields_extractor1)
    
    // ===== Mongo Importer module mongo_loader =====
    
    val mongo_loader = MongoReader[(String,String)](env, "testdb", "publications", List("lienPageTwitter","denomination")).getDataSet()
    
    // ===== Split split_twitter_hatvp =====
    
    val split_twitter_hatvp = mongo_loader.map { set => (set._1.toLowerCase.split("/")(set._1.toLowerCase.split("/").length - 1),set._2)}
    
    // ===== Split split_twitter_hatvp2 =====
    
    val split_twitter_hatvp2 = split_twitter_hatvp.map { set => (set._1.toLowerCase.split("\\?").length match { case 1 => set._1.toLowerCase.split("\\?")(0) case _ => set._1.toLowerCase.split("\\?")(0)},set._2)}
    
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
    val query_extractordb = "select rt_name, screen_name from (select rt_name, uid from (select us.screen_name as rt_name, rt.sid from retweetedstatuses as rt join users as us on (rt.uid=us.uid)) as sub join checkedstatuses as ch on (sub.sid=ch.sid)) as subsub join users on (subsub.uid=users.uid);"
    val interm_extractordb = SQLDBReader[(String,String)](fieldNames_extractordb, fieldTypes_extractordb, "org.postgresql.Driver", "jdbc:postgresql://localhost/twitter", query_extractordb, env).getDataSet
    
    val extractordb = interm_extractordb.map((elem: Row)=> getRequired[(String,String)](elem))

    // ===== CSV Importer module extractor4 =====
    
    val filePath_extractor4 = "/Users/hugo/Work/limsi-inria/tests/data_journalism_extractor/example/data/wiki.csv"
    val lineDelimiter_extractor4 = "\n"
    val fieldDelimiter_extractor4 = "|"
    val quoteCharacter_extractor4 = '$'
    val extractor4 = env.readCsvFile[(String,String)](filePath_extractor4, lineDelimiter_extractor4, fieldDelimiter_extractor4, quoteCharacter_extractor4)
    
    // ===== Word similarity extractor tryExtractorWordSim =====

    val tryExtractorWordSim = split_lex.cross(split_lex) {
        (c1, c2) => 
            val set1 = c1._2.toSet
            val set2 = c2._2.toSet
            val dist = set1.intersect(set2).size / set1.union(set2).size
        (c1, c2, dist)
    }
    
    // ===== Entity extractor linking1 =====
    
    val linking1 = extractor4.cross(mongo_loader).flatMap(new extract_extractor4_mongo_loader)
    
    // ===== Projection projection1 =====
    
    val projection1 = linking1.map { set => (set._1,set._3)}.distinct()
    
    // ===== CSV Output File output1 =====
    
    val filePath_output1 = "/Users/hugo/Work/limsi-inria/tests/data_journalism_extractor/example/output/output.csv"
    projection1.writeAsCsv(filePath_output1, writeMode=FileSystem.WriteMode.OVERWRITE)

    // ===== Execution =====

    env.execute()
  }

  
  
  // ===== Entity extractor FlatMapFunction linking1=====
  
  private class extract_extractor4_mongo_loader extends FlatMapFunction[((String,String), (String,String)), (String,String,String,String)] {
      override def flatMap(value: ((String,String), (String,String)), out: Collector[(String,String,String,String)]): Unit = {
        val d = (raw"\b(" + value._2._1.toLowerCase + raw")\b").r
        if (d.findFirstIn(value._1._2.toLowerCase).nonEmpty) out.collect((value._1._1,value._1._2,value._2._1,value._2._2))
      }
  }
  
  // ===== DB Importer module ext =====
  
  private def getRequired[T](elem: Row): T = {
      def tuplify = (i: Int) => elem.getField(i)
      val d = elem.getArity match {
        case 1 => Tuple1(tuplify(0))
        case 2 => (tuplify(0), tuplify(1))
        case 3 => (tuplify(0), tuplify(1), tuplify(2))
        case 4 => (tuplify(0), tuplify(1), tuplify(2), tuplify(3))
        case 5 => (tuplify(0), tuplify(1), tuplify(2), tuplify(3), tuplify(4))
        case 6 => (tuplify(0), tuplify(1), tuplify(2), tuplify(3), tuplify(4), tuplify(5))
      }
      d.asInstanceOf[T]
  }
}