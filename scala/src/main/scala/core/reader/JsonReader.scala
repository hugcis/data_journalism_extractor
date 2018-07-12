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
    val getFull = {d: Option[Json] => {d.get.string.getOrElse(d.get.toString())}}
    val d = requiredFields.length match {
      case 1 => Tuple1(getFull(elem.field(requiredFields(0))))
      case 2 => (getFull(elem.field(requiredFields(0))),
                 getFull(elem.field(requiredFields(1))))
      case 3 => (getFull(elem.field(requiredFields(0))),
                 getFull(elem.field(requiredFields(1))),
                 getFull(elem.field(requiredFields(2))))
      case 4 => (getFull(elem.field(requiredFields(0))),
                 getFull(elem.field(requiredFields(1))),
                 getFull(elem.field(requiredFields(2))),
                 getFull(elem.field(requiredFields(3))))
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