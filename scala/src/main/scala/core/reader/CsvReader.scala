/*
package core.reader

import org.apache.flink.api.java.{DataSet, ExecutionEnvironment}
import org.apache.flink.api.java.io.TupleCsvInputFormat
import org.apache.flink.api.java.tuple.Tuple
import org.apache.flink.api.java.typeutils.TupleTypeInfo
import org.apache.flink.core.fs.Path

case class CsvReader(env: ExecutionEnvironment,
                     file: String,
                     tupleInfo: TupleTypeInfo[Tuple],
                     lineDelimiter: String = "\n",
                     fieldDelimiter: String = ",",
                     skipFirstLine: Boolean = false,
                     quoteCharacter: Char = ' ') {

  val format = new TupleCsvInputFormat(
    new Path(file),
    lineDelimiter,
    fieldDelimiter,
    tupleInfo)

  format.setSkipFirstLineAsHeader(skipFirstLine)

  if (quoteCharacter != ' ') format.enableQuotedStringParsing(quoteCharacter)

  def getInput: DataSet[Tuple] =  env.createInput(format, tupleInfo)

}
*/
