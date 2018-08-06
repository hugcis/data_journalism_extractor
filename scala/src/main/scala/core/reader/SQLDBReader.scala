package core.reader

import org.apache.flink.api.common.io.InputFormat
import org.apache.flink.api.common.typeinfo.TypeInformation
import org.apache.flink.api.java.io.jdbc.JDBCInputFormat
import org.apache.flink.api.java.typeutils.RowTypeInfo
import org.apache.flink.api.scala.{DataSet, ExecutionEnvironment}
import org.apache.flink.types.Row

import scala.reflect.ClassTag

class SQLDBReader[T:ClassTag:TypeInformation](fieldNames: Array[String],
                                 fieldTypes: Array[TypeInformation[_]],
                                 driver: String,
                                 dbUrl: String,
                                 query: String,
                                 env: ExecutionEnvironment) {


  def getDataSet = {
    val rowTypeInfo = new RowTypeInfo(fieldTypes, fieldNames)
    val inputFormat = JDBCInputFormat.buildJDBCInputFormat()
      .setDrivername(driver)
      .setDBUrl(dbUrl)
      .setQuery(query)
      .setRowTypeInfo(rowTypeInfo)
      .finish()

    implicit val typeInfo = rowTypeInfo
    env.createInput[Row](inputFormat)
  }

  private def getRequired(elem: Row): T = {
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

object SQLDBReader {
  implicit def apply[T:ClassTag:TypeInformation](fieldNames: Array[String],
                     fieldTypes: Array[TypeInformation[_]],
                     driver: String,
                     dbUrl: String,
                     query: String,
                     env: ExecutionEnvironment): SQLDBReader[T] = new SQLDBReader[T](fieldNames, fieldTypes, driver, dbUrl, query, env)
}