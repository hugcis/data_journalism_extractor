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

  def getRequired(elem: Json) = {
    val d = requiredFields.length match {
      case 1 => Tuple1(elem.field(requiredFields(0)).get.string.get)
      case 2 => (elem.field(requiredFields(0)).get.string.get,
                 elem.field(requiredFields(1)).get.string.get)
      case 3 => (elem.field(requiredFields(0)).get.string.get,
                 elem.field(requiredFields(1)).get.string.get,
                 elem.field(requiredFields(2)).get.string.get)
      case 4 => (elem.field(requiredFields(0)).get.string.get,
                 elem.field(requiredFields(1)).get.string.get,
                 elem.field(requiredFields(2)).get.string.get,
                 elem.field(requiredFields(3)).get.string.get,)
    }
    d.asInstanceOf[T]
  }

  def getElements = Parse
    .parseOption(fetchSource)
    .get
    .field(mainArrayField)
    .get
    .array.get.toArray.map(getRequired)



  def getInput = env.fromCollection[T](getElements)
}

object JsonReader {
  implicit def apply[T: ClassTag: TypeInformation](env: ExecutionEnvironment,
            file: String,
            mainArrayField: String,
            requiredFields: Array[String]): JsonReader[T] = new JsonReader[T](env, file, mainArrayField, requiredFields)
}