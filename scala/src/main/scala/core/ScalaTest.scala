/*
package core

//import core.module.JSONModule
//import core.reader.JsonReader
//import org.apache.flink.api.common.functions.MapFunction
//mport org.apache.flink.api.java.ExecutionEnvironment
//import org.apache.flink.api.java.operators.DataSource
import org.apache.flink.api.scala._

object ScalaTest {

  def main(args: Array[String]) {

    // set up the execution environment
    //val env = ExecutionEnvironment.getExecutionEnvironment

/*    val t = TypeDescriptor(3, Array("string", "string", "string"))
    val csvFilePath =  "/Users/hugo/Work/limsi-inria/tests/test/deputes.csv"
    val lineDelimiter = "\n"
    val fieldDelimiter = ";"
    {% for module in modules %}
    {% endif %}
    val d = CsvReader(
      env,
      csvFilePath,
      t.getTupleTypeInfo,
      lineDelimiter,
      fieldDelimiter,
      true).getInput

    d.print()

    val t2 = TypeDescriptor(2, Array("string", "string"))
    val csvFilePath2 =  "/Users/hugo/Work/limsi-inria/tests/test/wiki.csv"
    val fieldDelimiter2 = "|"
    val quoteChar = '$'

    val s = CsvReader(
      env,
      csvFilePath2,
      t2.getTupleTypeInfo,
      fieldDelimiter = fieldDelimiter2,
      quoteCharacter = quoteChar).getInput

    s.print()

    val xmlFilePath = "/Users/hugo/Work/limsi-inria/tests/test/deputes.xml"
    val m = new XmlReader(env, xmlFilePath, Array("/deputes/depute/nom/text()", "/deputes/depute/slug/text()"))
    val qr = m.getInput
    qr.print()*/


//    val jsonFilePath = "/Users/hugo/Work/limsi-inria/tests/test/hatvp.json"
//    val data = JSONModule(jsonFilePath, "publications", Array("denomination", "identifiantNational")).dataSource(env)
//    data.print()
//    println(data.getClass)
//.print()
  }
}
*/
