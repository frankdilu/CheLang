from CheLang.Values import String, Number, BuiltInFunction, Empty
from CheLang.SymbolTable import SymbolTable
###############################
# BUILT-IN CONST 
###############################
global_symbol_table = SymbolTable()
global_symbol_table.set("Milanesa",String("Carne"))
global_symbol_table.set("Macri",String("Gato"))
global_symbol_table.set("AltoGuiso",Number(15))
global_symbol_table.set("Vacio", Empty())
global_symbol_table.set("Inviable", Number.null)
global_symbol_table.set("Chamuyo", Number.false)
global_symbol_table.set("Posta", Number.true)
global_symbol_table.set("Pi", Number.math_PI)
global_symbol_table.set("Cuchame", BuiltInFunction.print)
global_symbol_table.set("CuchameRet", BuiltInFunction.print_ret)
global_symbol_table.set("Traeme", BuiltInFunction.input)
global_symbol_table.set("TraemeNumerito", BuiltInFunction.input_int)
global_symbol_table.set("Limpiame", BuiltInFunction.clear)
global_symbol_table.set("clear", BuiltInFunction.clear)
global_symbol_table.set("EsNumerito", BuiltInFunction.is_number)
global_symbol_table.set("EsTexto", BuiltInFunction.is_string)
global_symbol_table.set("EsLista", BuiltInFunction.is_list)
global_symbol_table.set("EsFuncion", BuiltInFunction.is_function)
global_symbol_table.set("Agregale", BuiltInFunction.append)
global_symbol_table.set("Rajale", BuiltInFunction.pop)
global_symbol_table.set("Metele", BuiltInFunction.extend)
global_symbol_table.set("TaLargo", BuiltInFunction.len)
global_symbol_table.set("Correme", BuiltInFunction.run)
global_symbol_table.set("Hola", BuiltInFunction.hola)
global_symbol_table.set("Argentina", BuiltInFunction.argentina)
global_symbol_table.set("Chorro", BuiltInFunction.thief)
global_symbol_table.set("Ninos", BuiltInFunction.exit)
global_symbol_table.set("Boludear", BuiltInFunction.sleep)
global_symbol_table.set("Viborita", BuiltInFunction.python)
global_symbol_table.set("ANumerito", BuiltInFunction.toInt)
global_symbol_table.set("AFlotantito", BuiltInFunction.toFloat)
global_symbol_table.set("ATextito", BuiltInFunction.toStr)
global_symbol_table.set("FloatYPico", BuiltInFunction.FloatYPico)
global_symbol_table.set("Dolar", BuiltInFunction.dolar)
global_symbol_table.set("Campora", BuiltInFunction.campora)
global_symbol_table.set("HalloEbribodi", BuiltInFunction.HalloEbribodi)
global_symbol_table.set("Sumate", BuiltInFunction.sum)
global_symbol_table.set("ElMasGrande", BuiltInFunction.ElMasGrande)
global_symbol_table.set("HaceloInclusivoMacho", BuiltInFunction.HaceloInclusivoMacho)
global_symbol_table.set("EInclusivo", BuiltInFunction.EInclusivo)
