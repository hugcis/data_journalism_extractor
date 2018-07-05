/*
package core

import org.apache.flink.api.common.typeinfo.TypeInformation
import org.apache.flink.api.java.tuple.Tuple
import org.apache.flink.api.java.typeutils.{TupleTypeInfo, TypeExtractor}

case class TypeDescriptor(len: Int, type_array: Array[String]) {
  assert(len == type_array.length)

  val length: Int = len
  val types: Array[String] = type_array

  def getTuple: Tuple = {
    val top = Tuple.getTupleClass(length).newInstance()
    types.zipWithIndex.foreach { case (elem, idx) => top.setField(getAtomic(elem), idx)}
    top
  }

  def getTupleType: TypeInformation[Tuple] = TypeExtractor.getForObject(getTuple)

  def getTupleTypeInfo: TupleTypeInfo[Tuple] = getTupleType.asInstanceOf[TupleTypeInfo[Tuple]]

  private def getAtomic(value: String) = value match {
    case "string" => ""
    case "int" => 1
    case _ => 1
  }
}*/
