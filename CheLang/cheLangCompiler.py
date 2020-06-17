from CheLang.Values import String, Number, BuiltInFunction , Empty
from CheLang.SymbolTable import SymbolTable
from CheLang.Lexer import Lexer
from CheLang.Parser import Parser
from CheLang.Interpreter import Interpreter
from CheLang.Context import Context

###################################################
# RUN                      - usain bolt un poroto -
###################################################

global_symbol_table = SymbolTable()
global_symbol_table.set("Milanesa",String("Carne"))
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
global_symbol_table.set("len", BuiltInFunction.len)
global_symbol_table.set("run", BuiltInFunction.run)
global_symbol_table.set("Hola", BuiltInFunction.hola)
global_symbol_table.set("Argentina", BuiltInFunction.argentina)
global_symbol_table.set("Chorro", BuiltInFunction.thief)

def run(fn, text):
    #Generate tokens
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    if error: return None, error

    # Generate AST
    parser = Parser(tokens)
    ast = parser.parse()
    if ast.error: return None, ast.error

    # Run program
    interpreter = Interpreter()
    context = Context("main")
    context.symbol_table = global_symbol_table
    result = interpreter.visit(ast.node, context)

    return result.value, result.error