/*
package core.reader

import java.util

import core.TypeDescriptor
import kantan.xpath.Query
import kantan.xpath.implicits._
import org.apache.flink.api.java.ExecutionEnvironment
import org.apache.flink.api.java.operators.DataSource
import org.apache.flink.api.java.tuple.Tuple
import org.apache.flink.api.java.typeutils.TupleTypeInfo

import scala.collection.JavaConverters._

class XmlReader(env: ExecutionEnvironment,
                file: String,
                queries: Array[String],
                var tupleInfo: TupleTypeInfo[Tuple] = null) {

  assert(
    tupleInfo == null || queries.length == tupleInfo.getArity,
    "You should have as many queries as the number of elements in the tuple")
  if (tupleInfo == null) {
    tupleInfo = TypeDescriptor(
      queries.length,
      Array.fill[String](queries.length)("string")
    ).getTupleTypeInfo
  }


  private def getQueryResult(source: String, query: String): List[String] = {
    val xPathQuery = Query.compile[List[String]](query)

    xPathQuery match {
      case Right(x) => source.evalXPath(x).right.get
      case Left(x) => throw x
    }
  }

  private def fetchSource() = {
    val source = scala.io.Source.fromFile(file)
    try source.mkString finally source.close
  }

  private def getElements: util.Collection[Tuple] = {
    var arr = List[Tuple]()
    val source = fetchSource()
    val queryResults = queries.map(getQueryResult(source, _))

    queryResults(0).indices.foreach(i => {
      val tuple = tupleInfo.getTypeClass.newInstance()
      queryResults.indices.foreach(j => tuple.setField(queryResults(j)(i), j))
      arr = arr :+ tuple
    })

    arr.asJavaCollection
  }

  def getInput: DataSource[Tuple] = env.fromCollection(getElements, tupleInfo)

}

*/
