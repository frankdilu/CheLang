from CheLang.Lexer import Lexer
from CheLang.Parser import Parser
from CheLang.Interpreter import Interpreter
from CheLang.Context import Context
from CheLang.BuiltInConst import global_symbol_table

###################################################
# RUN                      - usain bolt un poroto -
###################################################
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