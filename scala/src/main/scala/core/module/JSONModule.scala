/*
package core.module

import core.reader.JsonReader
import org.apache.flink.api.java.operators.DataSource
import org.apache.flink.api.java.tuple.Tuple
//import org.apache.flink.api.java.typeutils.TupleTypeInfo
import org.apache.flink.api.java.{DataSet, ExecutionEnvironment}

class JSONModule(inputPath: String,
                 mainField: String,
                 requiredFields: Array[String],
  //               tupleInfoInput: TupleTypeInfo[Tuple]) extends ModuleFileImporter {
  /*val kind = "json"
  val path: String = inputPath
  val t*/upleInfo: TupleTypeInfo[Tuple] = tupleInfoInput

  override def dataSource(env: ExecutionEnvironment): DataSet[Tuple] =
    new JsonReader(env, path, mainField, requiredFields).getInput
}

object JSONModule {
  def apply(inputPath: String,
            mainField: String,
            requiredFields: Array[String],
            tupleInfoInput: TupleTypeInfo[Tuple] = null): JSONModule =
    new JSONModule(inputPath, mainField, requiredFields, tupleInfoInput)
}
*/
