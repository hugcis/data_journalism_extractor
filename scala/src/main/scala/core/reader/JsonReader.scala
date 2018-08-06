package core.reader

import argonaut._
import org.apache.flink.api.common.typeinfo.TypeInformation
import org.apache.flink.api.scala._

import scala.reflect.ClassTag

class JsonReader[T:ClassTag:TypeInformation](env: ExecutionEnvironment,
                             file: String,
                             mainArrayField: String,
                             requiredFields: Array[String]) {

  private def fetchSource = {
    val source = scala.io.Source.fromFile(file)
    try source.mkString finally source.close
  }

  private def getRequired(elem: Json) = {
    val getFull = {d: Option[Json] => {
      d.get.string.getOrElse(
        d.get.toString()
      )
    }}
    val tuplify = {i: Int => getFull(elem.field(requiredFields(i)))}
    val d = requiredFields.length match {
      case 1 => Tuple1(tuplify(0))
      case 2 => (tuplify(0), tuplify(1))
      case 3 => (tuplify(0), tuplify(1), tuplify(2))
      case 4 => (tuplify(0), tuplify(1), tuplify(2), tuplify(3))
      case 5 => (tuplify(0), tuplify(1), tuplify(2), tuplify(3), tuplify(4))
      case 6 => (tuplify(0), tuplify(1), tuplify(2), tuplify(3), tuplify(4), tuplify(5))
    }
    d.asInstanceOf[T]
  }

  private def getElements = Parse
    .parseOption(fetchSource)
    .get
    .field(mainArrayField)
    .get
    .array.get.toArray.map(getRequired)



  def getDataSet = env.fromCollection[T](getElements)
}

object JsonReader {
  implicit def apply[T: ClassTag: TypeInformation](env: ExecutionEnvironment,
            file: String,
            mainArrayField: String,
            requiredFields: Array[String]): JsonReader[T] = new JsonReader[T](env, file, mainArrayField, requiredFields)
}