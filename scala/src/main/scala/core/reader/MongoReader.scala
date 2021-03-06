package core.reader

import org.apache.flink.api.common.typeinfo.TypeInformation
import org.apache.flink.api.scala.{DataSet, ExecutionEnvironment}
import org.bson.BsonValue
import org.mongodb.scala.bson.conversions
import org.mongodb.scala.{Document, MongoClient, MongoDatabase, SingleObservable}
import org.mongodb.scala.model.{Filters, Projections}

import scala.concurrent.duration._
import scala.concurrent.ExecutionContext.Implicits.global
import scala.concurrent.Await
import scala.reflect.ClassTag
import collection.JavaConverters._

class MongoReader[T:ClassTag:TypeInformation](env: ExecutionEnvironment,
                                              dbName: String,
                                              collectionName: String,
                                              fields: List[String]) {
  private val mongoClient: MongoClient = MongoClient()
  private val database: MongoDatabase = mongoClient.getDatabase(dbName)
  private var finalCollection: List[T] = null

  def getDataSet(): DataSet[T] = {
    getElements()
    env.fromCollection(finalCollection)
  }

  private def getElements(): Unit = {
    val collection = database.getCollection(collectionName)
    val result = collection.find(getFilter(fields))
      .projection(Projections.fields(Projections.include(fields: _*), Projections.excludeId()))
      .collect().toFuture()
      .map((results: Seq[Document]) => finalCollection = results.toList.map(documentToCollection))
    Await.result(result, 3000 millis)
  }

  private def documentToCollection(doc: Document): T = {
    getRequired(fields.map(fieldExtractor(doc)).map(bsonValueToValue))
  }

  private def fieldExtractor(doc: Document): String => BsonValue = (field: String) => doc.get(field).get

  private def bsonValueToValue(elem: BsonValue): Either[String, Array[String]] = {
    if (elem.isArray) {
      Right(elem.asArray.getValues.asScala.toArray.map((elem: BsonValue) => {
        if (elem.isString) elem.asString.getValue else elem.asDocument.toJson
      }))
    } else if (elem.isDocument) {
      Left(elem.asDocument.toJson)
    } else Left(elem.asString.getValue)
  }

  private def getRequired(elem: List[Either[String, Array[String]]]): T = {
    val tuplify = (i: Int) => elem.apply(i) match {
      case Right(x) => x
      case Left(x) => x
    }
    val d = fields.length match {
      case 1 => Tuple1(tuplify(0))
      case 2 => (tuplify(0), tuplify(1))
      case 3 => (tuplify(0), tuplify(1), tuplify(2))
      case 4 => (tuplify(0), tuplify(1), tuplify(2), tuplify(3))
      case 5 => (tuplify(0), tuplify(1), tuplify(2), tuplify(3), tuplify(4))
      case 6 => (tuplify(0), tuplify(1), tuplify(2), tuplify(3), tuplify(4), tuplify(5))
    }
    d.asInstanceOf[T]
  }

  private def getFilter(fields: List[String]): conversions.Bson = {
    fields.length match {
      case 0 => null
      case 1 => Filters.exists(fields.head)
      case _ => Filters.and(
        Filters.exists(fields.head),
        getFilter(fields.slice(1, fields.length))
      )
    }
  }

}


object MongoReader {
  implicit def apply[T: ClassTag: TypeInformation](env: ExecutionEnvironment,
                                                   dbName: String,
                                                   collectionName: String,
                                                   fields: List[String]): MongoReader[T] =
    new MongoReader[T](env, dbName, collectionName, fields)
}
