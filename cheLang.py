from stringsWithArrows import * # eto pone flechitas en los errore
import string
import random
import os
import math
###################################################
# CONSTANTS - me dijeron que significa constantes -
###################################################

DIGITS = "0123456789" # los numerito
LETTERS = string.ascii_letters + "ñÑ"
LETTERS_DIGITS = LETTERS + DIGITS

###################################################
# ERRORS                            - bad news D: -
###################################################
###############################
# ERROR MESSAGES     - sfw :D -
###############################
# violentitud : media
errorMessages = {
    "IllegalCharError" : "Che pibe pusiste algo nada que ver, le mandaste",
    "InvalidSyntaxError" : "Flaco tu sintaxis no la entiende ni tu abuelita (saludos)",
    "RuntimeError" : "TE VAMOS A LINCHAR SI NO LO ARREGLAS BIGOTE",
    "ExpectedCharError" : "Te faltó poner algo: "
}
###############################
# ERROR DETAILS     - sfw :D -
###############################
detailsMessages = {
    "intOrFloatExpected" : "\nFlaco pasame un numerito ahi viste",
    "exprExpected" : "\nFlaco pasame un algo ahi viste",
    "operationExpected": "\nFlaco dame alguna operacion, lamentablemente no puedo hacer lo que me pinte",
    "closeParentesisExpected": "\nFlaco porque no cerras los partentesis?",
    "identifierExpected": "\nDecime un nombre pa la variable viste",
    "equalExpected": "\nTenes que poner 'es' o 'seigual' pa poner algo crack",
    "equalAfterNotExpected": "\nChe no sabes español? Tenes que poner 'No es'",
    "zeroDiv": "\ndividís por cero vos? Usted se tiene que arrepentir de lo que dijo",
    "unknownVariable": "\nCapo no me dijiste que es '",
    "languajeSyntaxError": "\nGenio leete la doc antes de escribir dale? Te faltó un '"
}

###############################
# ERROR SCHEME
###############################
class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    def as_string(self):
        result = f"{self.error_name}: {self.details} \n"
        result += f"En {self.pos_start.fn}, linea {self.pos_start.ln + 1} o por ahí\n" #era re croto viste
        result += "\n" + string_with_arrows(self.pos_start.ftxt, self.pos_start, self.pos_end)
        return result


###############################
# ILLEGAL CHAR ERROR
###############################
class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, errorMessages["IllegalCharError"], details)


###############################
# EXPECTED CHAR ERROR
###############################
class ExpectedCharError(Error):
    def __init__(self, pos_start, pos_end, details=""):
        super().__init__(pos_start, pos_end, errorMessages["ExpectedCharError"], details)


###############################
# INVALID SYNTAX ERROR
###############################
class InvalidSyntaxError(Error):
    def __init__(self, pos_start, pos_end, details=""):
        super().__init__(pos_start, pos_end, errorMessages["InvalidSyntaxError"], details)


###############################
# RUNTIME ERROR  - uh crashio -
###############################
class RTError(Error):
    def __init__(self, pos_start, pos_end, details, context):
        super().__init__(pos_start, pos_end, errorMessages["RuntimeError"], details)
        self.context = context

    def as_string(self):
        result = self.generate_traceback()
        result += f"{self.error_name}: {self.details}\n"
        result += "\n" +  string_with_arrows(self.pos_start.ftxt, self.pos_start, self.pos_end)
        return result

    ###############################
    # TRACEBACK  - pa saber donde - 
    ###############################
    def generate_traceback(self):
        result = ""
        pos = self.pos_start
        ctx = self.context

        while ctx:
            result = f" File {pos.fn}, line {str(pos.ln + 1)}, in {ctx.display_name}\n" + result
            pos = ctx.parent_entry_pos
            ctx = ctx.parent

        return "Traceback (most recent call last):\n" + result

###################################################
# POSITION
###################################################
class Position:
    def __init__(self, inx, ln, col, fn, ftxt):
        self.inx = inx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt

    ###############################
    # ADVANCE METHOD
    ###############################
    def advance(self, current_char=None):
        self.inx += 1
        self.col += 1

        if current_char == "\n":
            self.ln +=1
            self.col = 0

        return self

    ###############################
    # COPY METHOD
    ###############################
    def copy(self):
        return Position(self.inx, self.ln, self.col, self.fn, self.ftxt)

###################################################
# TOKENS
###################################################

###############################
# TOKENS TYPES
###############################
TT_INT = "TT_INT"
TT_FLOAT = "FLOAT"
TT_STRING = "STRING"
TT_IDENTIFIER = "IDENTIFIER"
TT_KEYWORD = "KEYWORD"
TT_PLUS = "PLUS"
TT_MINUS = "MINUS"
TT_MUL = "MUL"
TT_DIV = "DIV"
TT_POW = "POW"
TT_EQ = "EQ"
TT_LPAREN = "LPAREN"
TT_RPAREN = "RPAREN"
TT_LSQUARE = "LSQUARE"
TT_RSQUARE = "RSQUARE"
TT_EE = "EE"
TT_MM = "MM"
TT_NE = "NE"
TT_LT = "LT"
TT_GT = "GT"
TT_LTE = "LTE"
TT_GTE = "GTE"
TT_COMMA = "COMMA"
TT_ARROW = "ARROW"
TT_EOF = "EOF"

###############################
# KEYWORDS
###############################
KEYWORDS = [
    "che",
    "y",
    "o",
    "no",
    "ponele",
    "tonce",
    "osi",
    "alosumo",
    "for",
    "to",
    "step",
    "mientras",
    "fun",

]

###############################
#TOKEN SCHEME
###############################
class Token:
    def __init__(self, type_, value = None, pos_start=None, pos_end=None):
        self.type = type_
        self.value = value

        if pos_start:
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy()
            self.pos_end.advance()
        
        if pos_end:
            self.pos_end = pos_end.copy()

    def matches(self, type_, value):
        return self.type == type_ and self.value.lower() == value

    def __repr__(self):
        if self.value: return f"{self.type}:{self.value}"
        return str(self.type)

###################################################
# LEXER                         - El nerd que lee -
###################################################

class Lexer:
    def __init__(self, fn, text):
        self.fn = fn
        self.text = text
        self.pos = Position(-1,0,-1, fn, text)
        self.current_char = None
        self.advance()

    ###############################
    # ADVANCE POSITION
    ###############################

    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.inx] if self.pos.inx < len(self.text) else None

    ###############################
    # TOKENS FACTORY    ¡choo choo!
    ###############################

    def make_tokens(self):
        tokens = []

        while self.current_char != None:
            if self.current_char in " \t":
                self.advance()
            elif self.current_char in DIGITS + ".":
                tok, err = self.make_number()
                if err: return [], err
                tokens.append(tok)
            elif self.current_char == "(":
                tokens.append(Token(TT_LPAREN, pos_start=self.pos, pos_end=self.pos))
                self.advance()
            elif self.current_char == ")":
                tokens.append(Token(TT_RPAREN, pos_start=self.pos, pos_end=self.pos))
                self.advance()
            elif self.current_char == "[":
                tokens.append(Token(TT_LSQUARE, pos_start=self.pos, pos_end=self.pos))
                self.advance()
            elif self.current_char == "]":
                tokens.append(Token(TT_RSQUARE, pos_start=self.pos, pos_end=self.pos))
                self.advance()
            elif self.current_char == '"':
                tokens.append(self.make_string())
            elif self.current_char == ",":
                tokens.append(Token(TT_COMMA, pos_start=self.pos, pos_end=self.pos))
                self.advance()
            elif self.current_char == "=":
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char == ">":
                    tokens.append(Token(TT_ARROW, pos_start=pos_start, pos_end=self.pos))
                    self.advance()
                else:
                    return [], InvalidSyntaxError(
                        pos_start, self.pos,
                        detailsMessages["languajeSyntaxError"] + ">'"
                        )
            elif self.current_char in LETTERS:
                op, err = self.make_operator()
                if err: return [], err
                for opTok in op:
                    tokens.append(opTok)
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start, self.pos, char) #pa los que no saben escribir

        tokens.append(Token(TT_EOF, pos_start=self.pos))
        return tokens, None

    ###############################
    # NUMBER FACTORY        ¡pi pi!
    ###############################

    def make_number(self):
        num_str = ""
        dot_count = 0
        pos_start = self.pos.copy()

        while self.current_char != None and self.current_char in (DIGITS + "."):
            if self.current_char == ".":
                if dot_count == 1: break #si tiene mas de un punto tamo' complicado'
                dot_count += 1
                num_str += "."
            else:
                num_str += self.current_char
            self.advance()
        if num_str[0] != ".":
            if dot_count == 0:
                return Token(TT_INT, int(num_str), pos_start, self.pos) , None
            else:
                return Token(TT_FLOAT, float(num_str), pos_start, self.pos) , None
        else:
            num_str = "0" + num_str 
            return Token(TT_FLOAT, float(num_str), pos_start, self.pos) , None

    
    ###############################
    # OPERATOR FACTORY      ¡op op!
    ###############################

    def make_operator(self, next_str=None):
        op_str = ""
        pos_start = self.pos.copy()

        if next_str == None:
            while self.current_char != None and self.current_char in LETTERS:
                op_str += self.current_char
                self.advance()
        else: op_str = next_str

        # Aca diferencia las cosas, es un quilombo
        if op_str.lower() == "ma":
            return [Token(TT_PLUS, pos_start=pos_start, pos_end=self.pos)] , None
        elif op_str.lower() == "meno":
            return [Token(TT_MINUS, pos_start=pos_start, pos_end=self.pos)] , None
        elif op_str.lower() == "por":
            return [Token(TT_MUL, pos_start=pos_start, pos_end=self.pos)] , None
        elif op_str.lower() == "dividido":
            return [Token(TT_DIV, pos_start=pos_start, pos_end=self.pos)] , None
        elif op_str.lower() == "ala":
            return [Token(TT_POW, pos_start=pos_start, pos_end=self.pos)] , None
        elif op_str.lower() == "anda":
            if self.take_str().lower() == "por":
                return [Token(TT_EE, pos_start=pos_start, pos_end=self.pos)] , None
            else: return [], InvalidSyntaxError(
                pos_start, self.pos,
                detailsMessages["languajeSyntaxError"] + "por'"
            )
        elif op_str.lower() == "seigual":
            return [Token(TT_EQ, pos_start=pos_start, pos_end=self.pos)] , None
        elif op_str.lower() == "no":
            tok, error = self.make_not_equals()
            if error: return [], error
            return tok, None
        elif op_str.lower() == "es":
            tok, error, next_str = self.make_equals()
            if error: return [], error
            if next_str != None: 
                secToks, secErr = self.make_operator(next_str)
                if secErr: return [], secErr
                for secTok in secToks:
                    tok.append(secTok)
            return tok, None
        else:
            tok_type = TT_KEYWORD if op_str.lower() in KEYWORDS else TT_IDENTIFIER
            if op_str.lower() == "ponele":
                if self.take_str().lower() != "que": return [], InvalidSyntaxError(
                    pos_start, self.pos,
                    detailsMessages["languajeSyntaxError"] + "que'"
                    )
            return [Token(tok_type, op_str, pos_start, self.pos)], None

    ###############################
    # STRING FACTORY     ¡st st!
    ###############################
    def make_string(self):
        string = ""
        pos_start = self.pos.copy()
        escape_character = False
        self.advance()

        escape_characters = {
            "n" : "\n",
            "t" : "\t"
        }

        while self.current_char != None and (self.current_char != '"' or escape_character):
            if escape_character:
                string += escape_characters.get(self.current_char, self.current_char)
                escape_character = False
            else:
                if self.current_char == "\\":
                    escape_character = True
                else:
                    string += self.current_char
            self.advance()

        self.advance()
        return Token(TT_STRING, string, pos_start, self.pos)


    ###############################
    # NOT EQUAL FACTORY     ¡no no!
    ###############################
    def make_not_equals(self):
        pos_start = self.pos.copy()
        ne_str = self.take_str()
        
        if ne_str.lower() == "es":
            return [Token(TT_NE, pos_start=pos_start, pos_end=self.pos)], None
        
        return None, ExpectedCharError(pos_start,self.pos,detailsMessages["equalAfterNotExpected"])

    ###############################
    # TAKE NEXT STRING  ¡take take!
    ###############################
    def take_str(self):
        new_str = ""
        self.advance()

        while self.current_char != None and self.current_char in LETTERS + "()":
            new_str += self.current_char
            self.advance()

        return new_str

    ###############################
    # EQUAL FACTORY         ¡eq eq!
    ###############################
    def make_equals(self):
        eq_str = self.take_str()
        tok_type = TT_EQ
        pos_start = self.pos.copy()
        next_str = None

        if eq_str.lower() == "uncachitomeno":
            tok_type = TT_LT
        elif eq_str.lower() == "menoroigual":
            tok_type = TT_LTE
        elif eq_str.lower() == "uncachitoma":
            tok_type = TT_GT
        elif eq_str.lower() == "mayoroigual":
            tok_type = TT_GTE
        elif eq_str.lower() == "maomeno":
            tok_type = TT_MM
        elif eq_str.lower() == "nakever":
            tok_type = TT_NE

        if tok_type == TT_EQ and eq_str != "":
            next_str = eq_str

        return [Token(tok_type, pos_start=pos_start, pos_end=self.pos)], None, next_str

###################################################
# NODES                           - las cuestione -
###################################################
###############################
# NUMBERS      - los numerito -
###############################
class NumberNode:
    def __init__(self, tok):
        self.tok = tok
        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end

    def __repr__(self):
        return f"{self.tok}"

###############################
# STRING      - los numerito -
###############################
class StringNode:
    def __init__(self, tok):
        self.tok = tok
        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end

    def __repr__(self):
        return f"{self.tok}"

###############################
# LIST NODE
###############################
class ListNode:
    def __init__(self, element_nodes, pos_start, pos_end):
        self.element_nodes = element_nodes

        self.pos_start = pos_start
        self.pos_end = pos_end

###############################
# VAR ACCESS NODE
###############################
class VarAccessNode:
    def __init__(self,var_name_tok):
        self.var_name_tok = var_name_tok
        
        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.var_name_tok.pos_end

###############################
# VAR ASSIGN NODE
###############################
class VarAssignNode:
    def __init__(self, var_name_tok, value_node):
        self.var_name_tok = var_name_tok
        self.value_node = value_node

        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.value_node.pos_end


###############################
# OPERATIONS     - las cuenta -
###############################
class BinOpNode:
    def __init__(self, left_node, op_tok, right_node):
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node
    
        self.pos_start = self.left_node.pos_start
        self.pos_end = self.right_node.pos_end

    def __repr__(self):
        return f"({self.left_node}, {self.op_tok}, {self.right_node})"

###############################
# UNARY OPERATIONS - los meno -
###############################
class UnaryOpNode:
    def __init__(self, op_tok, node):
        self.op_tok = op_tok
        self.node = node
    
        self.pos_start = self.op_tok.pos_start
        self.pos_end = self.node.pos_end

    def __repr__(self):
        return f"({self.op_tok}, {self.node})"

###############################
# IF NODE  -ifttt intensifies -
###############################
class IfNode:
    def __init__(self, cases, else_case):
        self.cases = cases
        self.else_case = else_case

        self.pos_start = self.cases[0][0].pos_start
        self.pos_end = self.else_case or self.cases[-1][0].pos_end

###############################
# FOR NODE  
###############################
class ForNode:
    def __init__(self, var_name_tok, start_value_node, end_value_node, step_value_node, body_node):
        self.var_name_tok = var_name_tok
        self.start_value_node = start_value_node
        self.end_value_node = end_value_node
        self.step_value_node = step_value_node
        self.body_node = body_node

        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.body_node.pos_end

###############################
# WHILE NODE  
###############################
class WhileNode:
    def __init__(self, condition_node, body_node):
        self.condition_node = condition_node
        self.body_node = body_node

        self.pos_start = self.condition_node.pos_start
        self.pos_end = self.body_node.pos_end

###############################
# FUNCITON NODE  
###############################
class FuncDefNode:
    def __init__(self, var_name_tok, arg_name_toks, body_node):
        self.var_name_tok = var_name_tok
        self.arg_name_toks = arg_name_toks
        self.body_node = body_node

        if self.var_name_tok:
            self.pos_start = self.var_name_tok.pos_start
        elif len(self.arg_name_toks) > 0:
            self.pos_start = self.arg_name_toks[0].pos_start
        else:
            self.pos_start = self.body_node.pos_end

        self.pos_end = self.body_node.pos_end

###############################
# CALL FUNCITON NODE  
###############################
class CallNode:
    def __init__(self, node_to_call, arg_nodes):
        self.node_to_call = node_to_call
        self.arg_nodes = arg_nodes

        self.pos_start = self.node_to_call.pos_start

        if len(self.arg_nodes) > 0:
            self.pos_end = self.arg_nodes[-1].pos_end
        else:
            self.pos_end = self.node_to_call.pos_end

###################################################
# PARSE RESULT   - ete se fija si hiciste macanas -
###################################################
class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None
        self.advance_count = 0

    ###############################
    # REGISTER ADVANCEMENT  -count-
    ###############################
    def register_advancement(self):
        self.advance_count += 1

    ###############################
    # REGISTER METHOD - toma nota -
    ###############################
    def register(self, res):
        self.advance_count += res.advance_count
        if res.error: self.error = res.error
        return res.node

    ###############################
    # SUCCESS METHOD   - ganadorr -
    ###############################
    def success(self, node):
        self.node = node
        return self

    ###############################
    # FAILURE METHOD  - fracasado -
    ###############################
    def failure(self, error):
        if not self.error or self.advance_count == 0:
            self.error = error
        return self


###################################################
# PARSER     - este es el que diferencia las cosa -
###################################################
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tok_inx = -1
        self.advance()
    ###############################
    # ADVANCE METHOD - pa delante -
    ###############################
    def advance(self):
        self.tok_inx += 1
        if self.tok_inx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_inx]
        return self.current_tok

    ###############################
    # PARSE METHOD
    ###############################
    def parse(self):
        res = self.expr()
        if not res.error and self.current_tok.type != TT_EOF:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                detailsMessages["operationExpected"]
            ))
        return res

    ###############################
    # POWER METHOD - qué potente. -
    ###############################
    def power(self):
        return self.bin_op(self.call, (TT_POW, ), self.factor)

    ###############################
    # CALL METHOD - so numerito -
    ###############################
    def call(self):
        res = ParseResult()
        atom = res.register(self.atom())
        if res.error: return res

        if self.current_tok.type == TT_LPAREN:
            res.register_advancement()
            self.advance()
            arg_nodes = []

            if self.current_tok.type == TT_RPAREN:
                res.register_advancement()
                self.advance()
            else:
                arg_nodes.append(res.register(self.expr()))
                if res.error:
                    return res.failure(InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        "Expected ')', 'VAR', 'IF', 'FOR', 'WHILE', 'FUN', int, float, identifier, '+', '-', '(' or 'NOT'"
                    ))

                while self.current_tok.type == TT_COMMA:
                    res.register_advancement()
                    self.advance()

                    arg_nodes.append(res.register(self.expr()))
                    if res.error: return res

                if self.current_tok.type != TT_RPAREN:
                    return res.failure(InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        f"Expected ',' or ')'"
                    ))

                res.register_advancement()
                self.advance()
            return res.success(CallNode(atom, arg_nodes))
        return res.success(atom)


    ###############################
    # ATOM METHOD - so numerito -
    ###############################
    def atom(self):
        res = ParseResult()
        tok = self.current_tok
        # Che, es un numerin?
        if tok.type in (TT_INT, TT_FLOAT):
            res.register_advancement()
            self.advance()
            return res.success(NumberNode(tok))
        # Che, es un numerin?
        if tok.type == TT_STRING:
            res.register_advancement()
            self.advance()
            return res.success(StringNode(tok))
        # Che, es una variable
        elif tok.type == TT_IDENTIFIER:
            res.register_advancement()
            self.advance()
            return res.success(VarAccessNode(tok))
        # Che, es un parentesi?
        elif tok.type == TT_LPAREN:  # si tiene un parentesi le da las prioridade
            res.register_advancement()
            self.advance()
            expr = res.register(self.expr())
            if res.error: return res
            if self.current_tok.type == TT_RPAREN:
                res.register_advancement()
                self.advance()
                return res.success(expr)
            else:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    detailsMessages["closeParentesisExpected"]
                ))
        # Che, es una lista?
        elif tok.type == TT_LSQUARE:
            list_expr = res.register(self.list_expr())
            if res.error:return res
            return res.success(list_expr)
        # Che, es un ponele?
        elif tok.matches(TT_KEYWORD, "ponele"):
            if_expr = res.register(self.if_expr())
            if res.error: return res
            return res.success(if_expr)

        # Che, es un for?
        elif tok.matches(TT_KEYWORD, "for"):
            for_expr = res.register(self.for_expr())
            if res.error: return res
            return res.success(for_expr)

        # Che, es un while?
        elif tok.matches(TT_KEYWORD, "mientras"):
            while_expr = res.register(self.while_expr())
            if res.error: return res
            return res.success(while_expr)
        
        # Che, es una funcion?
        elif tok.matches(TT_KEYWORD, "fun"):
            func_def = res.register(self.func_def())
            if res.error: return res
            return res.success(func_def)

        # Si llega acá hiciste macanas bro
        return res.failure(InvalidSyntaxError(
            tok.pos_start, tok.pos_end,
            detailsMessages["intOrFloatExpected"]
        ))

    ###############################
    # FACTOR METHOD - los factore -
    ###############################
    def factor(self):
        res = ParseResult()
        tok = self.current_tok

        # si tiene un mameno lo hace con el iunari ese
        if tok.type in (TT_PLUS, TT_MINUS):
            res.register_advancement()
            self.advance()
            factor = res.register(self.factor())
            if res.error: return res
            return res.success(UnaryOpNode(tok, factor))

        return self.power()

    ###############################
    # TERM METHOD  - so' multiplo -
    ###############################
    def term(self):
        return self.bin_op(self.factor, (TT_MUL,TT_DIV))

    ###############################
    # ARITH METHOD
    ###############################
    def arith_expr(self):
        return self.bin_op(self.term,(TT_PLUS, TT_MINUS))

    ###############################
    # LIST EXPR METHOD
    ###############################
    def list_expr(self):
        res = ParseResult()
        element_nodes = []
        pos_start = self.current_tok.pos_start.copy()

        if self.current_tok.type != TT_LSQUARE:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "[ expected"
            ))

        res.register_advancement()
        self.advance()

        if self.current_tok.type == TT_RSQUARE:
            res.register_advancement()
            self.advance()
        else:
            element_nodes.append(res.register(self.expr()))
            if res.error:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected ')', 'VAR', 'IF', 'FOR', 'WHILE', 'FUN', int, float, identifier, '+', '-', '(' or 'NOT'"
                ))

            while self.current_tok.type == TT_COMMA:
                res.register_advancement()
                self.advance()

                element_nodes.append(res.register(self.expr()))
                if res.error: return res

            if self.current_tok.type != TT_RSQUARE:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    f"Expected ',' or ')'"
                ))

            res.register_advancement()
            self.advance()
            return res.success(ListNode(
                element_nodes,
                pos_start,
                self.current_tok.pos_end.copy()
            ))

    ###############################
    # IF EXPR METHOD    - los ife -
    ###############################
    def if_expr(self):
        res = ParseResult()
        cases = []
        else_case = None

        if not self.current_tok.matches(TT_KEYWORD, "ponele"):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                detailsMessages["languajeSyntaxError"] + "ponele'"
            ))
        
        res.register_advancement()
        self.advance()

        condition = res.register(self.expr())
        if res.error:return res

        if not self.current_tok.matches(TT_KEYWORD, "tonce"):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                detailsMessages["languajeSyntaxError"] + "tonce'"
            ))

        res.register_advancement()
        self.advance()

        expr = res.register(self.expr())
        if res.error: return res
        cases.append((condition, expr))

        while self.current_tok.matches(TT_KEYWORD, "osi"):
            res.register_advancement()
            self.advance()

            condition = res.register(self.expr())
            if res.error: return res

            if not self.current_tok.matches(TT_KEYWORD, "tonce"):
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    detailsMessages["languajeSyntaxError"] + "tonce'"
                ))

            self.advance()
            expr = res.register(self.expr())
            if res.error: return res
            cases.append((condition,expr))

        if self.current_tok.matches(TT_KEYWORD, "alosumo"):
            res.register_advancement()
            self.advance()

            else_case = res.register(self.expr())
            if res.error: return res
        
        return res.success(IfNode(cases, else_case))

    ###############################
    # FOR METHOD
    ###############################
    def for_expr(self):
        res = ParseResult()

        if not self.current_tok.matches(TT_KEYWORD, "for"):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                detailsMessages["languajeSyntaxError"] + "for'"
            ))

        res.register_advancement()
        self.advance()

        if self.current_tok.type != TT_IDENTIFIER:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                detailsMessages["languajeSyntaxError"] + "nombre de variable'"
            ))

        var_name = self.current_tok
        res.register_advancement()
        self.advance()

        if self.current_tok.type != TT_EQ:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                detailsMessages["languajeSyntaxError"] + "es o seigual'"
            ))

        res.register_advancement()
        self.advance()

        start_value = res.register(self.expr())
        if res.error: return res

        if not self.current_tok.matches(TT_KEYWORD, "to"):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                detailsMessages["languajeSyntaxError"] + "to'"
            ))

        res.register_advancement()
        self.advance()

        end_value = res.register(self.expr())
        if res.error: return res

        if self.current_tok.matches(TT_KEYWORD, "step"):
            res.register_advancement()
            self.advance()

            step_value = res.register(self.expr())
            if res.error: return res
        else: 
            step_value = None
        
        if not self.current_tok.matches(TT_KEYWORD, "tonce"):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                detailsMessages["languajeSyntaxError"] + "tonce'"
            ))
        
        res.register_advancement()
        self.advance()

        body = res.register(self.expr())
        if res.error: return res

        return res.success(ForNode(var_name, start_value, end_value, step_value, body))

    ###############################
    # WHILE METHOD
    ###############################
    def while_expr(self):
        res = ParseResult()

        if not self.current_tok.matches(TT_KEYWORD, "mientras"):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                detailsMessages["languajeSyntaxError"] + "mientras'"
            ))

        res.register_advancement()
        self.advance()

        condition = res.register(self.expr())
        if res.error: return res

        if not self.current_tok.matches (TT_KEYWORD, "tonce"):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                detailsMessages["languajeSyntaxError"] + "tonce'"
            ))

        res.register_advancement()
        self.advance()

        body = res.register(self.expr())
        if res.error: return res
        
        return res.success(WhileNode(condition, body))

    ###############################
    # COMPARATOR METHOD
    ###############################
    def comp_expr(self):
        res = ParseResult()

        if self.current_tok.matches(TT_KEYWORD, "no"):
            op_tok = self.current_tok
            res.register_advancement()
            self.advance()

            node = res.register(self.comp_expr())
            if res.error: return res
            return res.success(UnaryOpNode(op_tok, node))

        node = res.register(self.bin_op(self.arith_expr, (TT_EE,TT_NE,TT_LT,TT_GT,TT_LTE,TT_GTE,TT_MM)))

        if res.error:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                detailsMessages["exprExpected"]
            ))

        return res.success(node)

    ###############################
    # EXPR METHOD      - so' suma -
    ###############################
    def expr(self):
        res = ParseResult()
        if self.current_tok.matches(TT_KEYWORD, "che"):
            res.register_advancement()
            self.advance()

            if self.current_tok.type != TT_IDENTIFIER:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    detailsMessages["identifierExpected"]
                ))
            var_name = self.current_tok
            res.register_advancement()
            self.advance()

            if self.current_tok.type != TT_EQ:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    detailsMessages["equalExpected"]
                ))
            res.register_advancement()
            self.advance()
            expr = res.register(self.expr())
            if res.error: return res
            return res.success(VarAssignNode(var_name, expr))

        node = res.register(self.bin_op(self.comp_expr, ((TT_KEYWORD, "y"),(TT_KEYWORD, "o"))))

        if res.error:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                detailsMessages["exprExpected"]
            ))

        return res.success(node)

    ###############################
    # FUNC DEFINITION METHOD 
    ###############################
    def func_def(self):
        res = ParseResult()

        if not self.current_tok.matches(TT_KEYWORD, 'fun'):
            return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected 'FUN'"
                    ))

        res.register_advancement()
        self.advance()

        if self.current_tok.type == TT_IDENTIFIER:
            var_name_tok = self.current_tok
            res.register_advancement()
            self.advance()
            if self.current_tok.type != TT_LPAREN:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    f"Expected '('"
                ))
        else:
            var_name_tok = None
            if self.current_tok.type != TT_LPAREN:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    f"Expected identifier or '('"
                ))
        
        res.register_advancement()
        self.advance()
        arg_name_toks = []

        if self.current_tok.type == TT_IDENTIFIER:
            arg_name_toks.append(self.current_tok)
            res.register_advancement()
            self.advance()
            
            while self.current_tok.type == TT_COMMA:
                res.register_advancement()
                self.advance()

                if self.current_tok.type != TT_IDENTIFIER:
                    return res.failure(InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        f"Expected identifier"
                    ))

                arg_name_toks.append(self.current_tok)
                res.register_advancement()
                self.advance()
            
            if self.current_tok.type != TT_RPAREN:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    f"Expected ',' or ')'"
                ))
        else:
            if self.current_tok.type != TT_RPAREN:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    f"Expected identifier or ')'"
                ))

        res.register_advancement()
        self.advance()

        if self.current_tok.type != TT_ARROW:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected '->'"
            ))

        res.register_advancement()
        self.advance()
        node_to_return = res.register(self.expr())
        if res.error: return res

        return res.success(FuncDefNode(
            var_name_tok,
            arg_name_toks,
            node_to_return
        ))


    ###############################
    # BIN_OP METHOD - junta cosas -
    ###############################
    def bin_op(self, func_a, ops, func_b=None):
        if func_b == None:
            func_b = func_a
        
        res = ParseResult()
        left = res.register(func_a())
        if res.error: return res
        
        while self.current_tok.type in ops or (self.current_tok.type, self.current_tok.value) in ops:
            op_tok = self.current_tok
            res.register_advancement()
            self.advance()
            right = res.register(func_b())
            if res.error: return res
            left = BinOpNode(left, op_tok, right)
        
        return res.success(left)

###################################################
# RUNTIME RESULT
###################################################
class RTResult:
    def __init__(self):
        self.value = None
        self.error = None

    ###############################
    # REGISTER METHOD 
    ###############################
    def register(self, res):
        if res.error: self.error = res.error
        return res.value

    ###############################
    # SUCCESS METHOD   - ganadorr -
    ###############################
    def success(self, value):
        self.value = value
        return self
    ###############################
    # FAILURE METHOD   - fracasau -
    ###############################
    def failure(self, error):
        self. error = error
        return self


###################################################
# VALUES
###################################################
#######################################
# VALUE BASE
#######################################
class Value:
    def __init__(self):
        self.set_pos()
        self.set_context()

    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

    def set_context(self, context=None):
        self.context = context
        return self

    def added_to(self, other):
        return None, self.illegal_operation(other)

    def subbed_by(self, other):
        return None, self.illegal_operation(other)

    def multed_by(self, other):
        return None, self.illegal_operation(other)

    def dived_by(self, other):
        return None, self.illegal_operation(other)

    def powed_by(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_eq(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_ne(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_lt(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_gt(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_lte(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_gte(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_mm(self, other):
        return None, self.illegal_operation(other)

    def anded_by(self, other):
        return None, self.illegal_operation(other)

    def ored_by(self, other):
        return None, self.illegal_operation(other)

    def notted(self, other):
        return None, self.illegal_operation(other)

    def execute(self, args):
        return RTResult().failure(self.illegal_operation())

    def copy(self):
        raise Exception('No copy method defined')

    def is_true(self):
        return False

    def illegal_operation(self, other=None):
        if not other: other = self
        return RTError(
            self.pos_start, other.pos_end,
            'Illegal operation',
            self.context
        )

###############################
# NUMBER CLASS - los numerito -
###############################
class Number(Value):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def added_to(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def subbed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def multed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def dived_by(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, RTError(
                    other.pos_start, other.pos_end,
                    'Division by zero',
                    self.context
                )

            return Number(self.value / other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def powed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value ** other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_ee(self, other):
        if isinstance(other, Number):
            return Number(int(self.value == other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_ne(self, other):
        if isinstance(other, Number):
            return Number(int(self.value != other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_lt(self, other):
        if isinstance(other, Number):
            return Number(int(self.value < other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_gt(self, other):
        if isinstance(other, Number):
            return Number(int(self.value > other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_lte(self, other):
        if isinstance(other, Number):
            return Number(int(self.value <= other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_gte(self, other):
        if isinstance(other, Number):
            return Number(int(self.value >= other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
        
    ###############################
    # MAOMENO METHOD   - the best -
    ###############################
    def get_comparison_mm(self, other):
        if isinstance(other,Number):
            if self.value >= other.value - other.value * .20 and self.value <= other.value + other.value * .20:
                return Number(1).set_context(self.context), None
            elif other.value >= self.value - self.value * .20 and other.value <= self.value + self.value * .20:
                return Number(1).set_context(self.context), None
            else:
                return Number(0).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)


    def anded_by(self, other):
        if isinstance(other, Number):
            return Number(int(self.value and other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def ored_by(self, other):
        if isinstance(other, Number):
            return Number(int(self.value or other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def notted(self):
        return Number(1 if self.value == 0 else 0).set_context(self.context), None


    def copy(self):
        copy = Number(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def is_true(self):
        return self.value != 0
        
    def __repr__(self):
        return str(self.value)

Number.null = Number(None)
Number.false = Number(0)
Number.true = Number(1)
Number.math_PI = Number(math.pi)

class String(Value):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def added_to(self, other):
        if isinstance(other, String):
            return String(self.value + other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def multed_by(self, other):
        if isinstance(other, Number):
            return String(self.value * other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def is_true(self):
        return len(self.value)>0

    def copy(self):
        copy = String(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def __repr__(self):
        return f'"{self.value}"'

    def __str__(self):
        return self.value

class List(Value):
    def __init__(self, elements):
        super().__init__()
        self.elements = elements

    def added_to(self, other):
        new_list = self.copy()
        if isinstance(other, List):
            new_list.elements.extend(other.elements)
        else:
            new_list.elements.append(other)
        return new_list, None

    def subbed_by(self,other):
        if isinstance(other, Number):
            new_list = self.copy()
            try:
                new_list.elements.pop(other.value)
                return new_list, None
            except:
                return None, RTError(
                    other.pos_start, other.pos_end,
                    "Index is outbounded ahjre",
                    self.context
                )
        else:
            return None, Value.illegal_operation(self, other)

    def multed_by(self, other):
        new_list = self.copy()
        new_list.elements.extend(new_list.elements * other.value)
        return new_list, None

    def dived_by(self, other):
        if isinstance(other, Number):
            try:
                return self.elements[other.value], None
            except:
                return None, RTError(
                    other.pos_start, other.pos_end,
                    "Index is outbounded ahjre",
                    self.context
                )
        else:
            return None, Value.illegal_operation(self, other)

    def copy(self):
        copy = List(self.elements)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def __str__(self):
        return f'[{", ".join([str(x) for x in self.elements])}]'
    def __repr__(self):
        return f'[{", ".join([str(x) for x in self.elements])}]'


class BaseFunction(Value):
    def __init__(self, name):
        super().__init__()
        self.name = name or "<anonymous>"

    def generate_new_context(self):
        new_context = Context(self.name, self.context, self.pos_start)
        new_context.symbol_table = SymbolTable(new_context.parent.symbol_table)
        return new_context

    def check_args(self, arg_names, args):
        res = RTResult()

        if len(args) > len(arg_names):
            return res.failure(RTError(
                self.pos_start, self.pos_end,
                f"{len(args) - len(arg_names)} too many args passed into {self}",
                self.context
            ))
        
        if len(args) < len(arg_names):
            return res.failure(RTError(
                self.pos_start, self.pos_end,
                f"{len(arg_names) - len(args)} too few args passed into {self}",
                self.context
            ))

        return res.success(None)

    def populate_args(self, arg_names, args, exec_ctx):
        for i in range(len(args)):
            arg_name = arg_names[i]
            arg_value = args[i]
            arg_value.set_context(exec_ctx)
            exec_ctx.symbol_table.set(arg_name, arg_value)

    def check_and_populate_args(self, arg_names, args, exec_ctx):
        res = RTResult()
        res.register(self.check_args(arg_names, args))
        if res.error: return res
        self.populate_args(arg_names, args, exec_ctx)
        return res.success(None)

class Function(BaseFunction):
    def __init__(self, name, body_node, arg_names):
        super().__init__(name)
        self.body_node = body_node
        self.arg_names = arg_names

    def execute(self, args):
        res = RTResult()
        interpreter = Interpreter()
        exec_ctx = self.generate_new_context()

        res.register(self.check_and_populate_args(self.arg_names, args, exec_ctx))
        if res.error: return res

        value = res.register(interpreter.visit(self.body_node, exec_ctx))
        if res.error: return res
        return res.success(value)

    def copy(self):
        copy = Function(self.name, self.body_node, self.arg_names)
        copy.set_context(self.context)
        copy.set_pos(self.pos_start, self.pos_end)
        return copy

    def __repr__(self):
        return f"<function {self.name}>"

class BuiltInFunction(BaseFunction):
    def __init__(self, name):
        super().__init__(name)

    def execute(self, args):
        res = RTResult()
        exec_ctx = self.generate_new_context()

        method_name = f'execute_{self.name}'
        method = getattr(self, method_name, self.no_visit_method)

        res.register(self.check_and_populate_args(method.arg_names, args, exec_ctx))
        if res.error: return res

        return_value = res.register(method(exec_ctx))
        if res.error: return res
        return res.success(return_value)
        
    def no_visit_method(self, node, context):
        raise Exception(f'No execute_{self.name} method defined')

    def copy(self):
        copy = BuiltInFunction(self.name)
        copy.set_context(self.context)
        copy.set_pos(self.pos_start, self.pos_end)
        return copy

    def __repr__(self):
        return f"<built-in function {self.name}>"

    #####################################

    def execute_print(self, exec_ctx):
        print(str(exec_ctx.symbol_table.get('value')))
        return RTResult().success(Number.null)
    execute_print.arg_names = ['value']
        
    def execute_print_ret(self, exec_ctx):
        return RTResult().success(String(str(exec_ctx.symbol_table.get('value'))))
    execute_print_ret.arg_names = ['value']
        
    def execute_input(self, exec_ctx):
        text = input("Que me queré decir bro? ")
        return RTResult().success(String(text))
    execute_input.arg_names = []

    def execute_input_int(self, exec_ctx):
        while True:
            text = input("Tirame un numero: ")
            try:
                number = int(text)
                break
            except ValueError:
                print(f"'{text}' tiene que ser un numero tarao, mandale denuevo")
        return RTResult().success(Number(number))
    execute_input_int.arg_names = []

    def execute_clear(self, exec_ctx):
        os.system('cls' if os.name == 'nt' else 'cls') 
        return RTResult().success(Number.null)
    execute_clear.arg_names = []

    def execute_is_number(self, exec_ctx):
        is_number = isinstance(exec_ctx.symbol_table.get("value"), Number)
        return RTResult().success(Number.true if is_number else Number.false)
    execute_is_number.arg_names = ["value"]

    def execute_is_string(self, exec_ctx):
        is_number = isinstance(exec_ctx.symbol_table.get("value"), String)
        return RTResult().success(Number.true if is_number else Number.false)
    execute_is_string.arg_names = ["value"]

    def execute_is_list(self, exec_ctx):
        is_number = isinstance(exec_ctx.symbol_table.get("value"), List)
        return RTResult().success(Number.true if is_number else Number.false)
    execute_is_list.arg_names = ["value"]

    def execute_is_function(self, exec_ctx):
        is_number = isinstance(exec_ctx.symbol_table.get("value"), BaseFunction)
        return RTResult().success(Number.true if is_number else Number.false)
    execute_is_function.arg_names = ["value"]

    def execute_append(self, exec_ctx):
        list_ = exec_ctx.symbol_table.get("list")
        value = exec_ctx.symbol_table.get("value")

        if not isinstance(list_, List):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "First argument must be list",
                exec_ctx
            ))

        list_.elements.append(value)
        return RTResult().success(Number.null)
    execute_append.arg_names = ["list", "value"]

    def execute_pop(self, exec_ctx):
        list_ = exec_ctx.symbol_table.get("list")
        index = exec_ctx.symbol_table.get("index")

        if not isinstance(list_, List):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "First argument must be list",
                exec_ctx
            ))

        if not isinstance(index, Number):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Second argument must be number",
                exec_ctx
            ))

        try:
            element = list_.elements.pop(index.value)
        except:
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                'Element at this index could not be removed from list because index is out of bounds',
                exec_ctx
            ))
        return RTResult().success(element)
    execute_pop.arg_names = ["list", "index"]

    def execute_extend(self, exec_ctx):
        listA = exec_ctx.symbol_table.get("listA")
        listB = exec_ctx.symbol_table.get("listB")

        if not isinstance(listA, List):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "First argument must be list",
                exec_ctx
            ))

        if not isinstance(listB, List):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Second argument must be list",
                exec_ctx
            ))

        listA.elements.extend(listB.elements)
        return RTResult().success(Number.null)
    execute_extend.arg_names = ["listA", "listB"]

BuiltInFunction.print       = BuiltInFunction("print")
BuiltInFunction.print_ret   = BuiltInFunction("print_ret")
BuiltInFunction.input       = BuiltInFunction("input")
BuiltInFunction.input_int   = BuiltInFunction("input_int")
BuiltInFunction.clear       = BuiltInFunction("clear")
BuiltInFunction.is_number   = BuiltInFunction("is_number")
BuiltInFunction.is_string   = BuiltInFunction("is_string")
BuiltInFunction.is_list     = BuiltInFunction("is_list")
BuiltInFunction.is_function = BuiltInFunction("is_function")
BuiltInFunction.append      = BuiltInFunction("append")
BuiltInFunction.pop         = BuiltInFunction("pop")
BuiltInFunction.extend      = BuiltInFunction("extend")

###################################################
# CONTEXT
###################################################

class Context:
    def __init__(self, display_name, parent=None, parent_entry_pos=None):
        self.display_name = display_name
        self.parent = parent
        self.parent_entry_pos = parent_entry_pos
        self.symbol_table = None

###################################################
# SYMBOL TABLE
###################################################
class SymbolTable:
    def __init__(self, parent = None):
        self.symbols = {}
        self.parent = parent

    ###############################
    # GET METHOD
    ###############################
    def get(self, name):
        value = self.symbols.get(name, None)
        if value == None and self.parent:
            return self.parent.get(name)
        return value

    ###############################
    # SET METHOD
    ###############################
    def set(self, name, value):
        self.symbols[name] = value

    ###############################
    # REMOVE METHOD
    ###############################
    def remove(self, name):
        del self.symbols[name]


###################################################
# INTERPRETER
###################################################

class Interpreter:
    def visit(self, node, context):
        method_name = f"visit_{type(node).__name__}"
        method = getattr(self,method_name, self.no_visit_method)
        return method(node, context)

    ###############################
    # NOT VISIT METHOD DEFINED
    ###############################
    def no_visit_method(self, node, context):
        raise Exception(f"No visit_{type(node).__name__} method defined")

    ###############################
    # NUMBER VISIT METHOD 
    ###############################
    def visit_NumberNode(self, node, context):
        return RTResult().success(
            Number(node.tok.value).set_context(context).set_pos(node.pos_start,node.pos_end)
        )

    def visit_StringNode(self, node, context):
        return RTResult().success(
            String(node.tok.value).set_context(context).set_pos(node.pos_start, node.pos_end)
        )

    def visit_ListNode(self, node, context):
        res = RTResult()
        elements = []

        for element_node in node.element_nodes:
            elements.append(res.register(self.visit(element_node, context)))
            if res.error: return res

        return res.success(
            List(elements).set_context(context).set_pos(node.pos_start, node.pos_end)
        )

    ###############################
    # VAR ACCESS VISIT METHOD 
    ###############################
    def visit_VarAccessNode(self,node,context):
        res = RTResult()
        var_name = node.var_name_tok.value
        value = context.symbol_table.get(var_name)

        if not value:
            return res.failure(RTError(
                node.pos_start, node.pos_end,
                detailsMessages["unknownVariable"] + var_name + "'",
                context
            ))

        value = value.copy().set_context(context).set_pos(node.pos_start, node.pos_end)
        return res.success(value)

    ###############################
    # VAR ASSIGN VISIT METHOD 
    ###############################
    def visit_VarAssignNode(self, node, context):
        res = RTResult()
        var_name = node.var_name_tok.value
        value = res.register(self.visit(node.value_node, context))
        if res.error: return res

        context.symbol_table.set(var_name,value)
        return res.success(value)

    ###############################
    # BIN OP VISIT METHOD 
    ###############################
    def visit_BinOpNode(self, node, context):
        res = RTResult()
        left = res.register(self.visit(node.left_node, context))
        if res.error: return res
        right = res.register(self.visit(node.right_node, context))
        if res.error: return res

        if node.op_tok.type == TT_PLUS:
            result, error = left.added_to(right)
        elif node.op_tok.type == TT_MINUS:
            result, error = left.subbed_by(right)
        elif node.op_tok.type == TT_MUL:
            result, error = left.multed_by(right)
        elif node.op_tok.type == TT_DIV:
            result, error = left.dived_by(right)
        elif node.op_tok.type == TT_POW:
            result, error = left.powed_by(right)
        elif node.op_tok.type == TT_EE:
            result, error = left.get_comparison_ee(right)
        elif node.op_tok.type == TT_NE:
            result, error = left.get_comparison_ne(right)
        elif node.op_tok.type == TT_LT:
            result, error = left.get_comparison_lt(right)
        elif node.op_tok.type == TT_GT:
            result, error = left.get_comparison_gt(right)
        elif node.op_tok.type == TT_LTE:
            result, error = left.get_comparison_lte(right)
        elif node.op_tok.type == TT_GTE:
            result, error = left.get_comparison_gte(right)
        elif node.op_tok.type == TT_MM:
            result, error = left.get_comparison_mm(right)
        elif node.op_tok.matches(TT_KEYWORD, "y"):
            result, error = left.anded_by(right)
        elif node.op_tok.matches(TT_KEYWORD, "o"):
            result, error = left.ored_by(right)

        if error:
            return res.failure(error)
        else:

            return res.success(result.set_pos(node.pos_start,node.pos_end))

    ###############################
    # UNARY OP VISIT METHOD 
    ###############################
    def visit_UnaryOpNode(self, node, context):
        res = RTResult()
        number = res.register(self.visit(node.node, context))
        if res.error: return res

        error = None

        if node.op_tok.type == TT_MINUS:
            number, error = number.multed_by(Number(-1))
        
        if node.op_tok.matches(TT_KEYWORD, "no"):
            number, error = number.notted()

        if error:
            return res.failure(error)
        else:
            return res.success(number.set_pos(node.pos_start,node.pos_end))

    ###############################
    # IF NODE VISIT METHOD 
    ###############################
    def visit_IfNode(self, node, context):
        res = RTResult()

        for condition, expr in node.cases:
            condition_value = res.register(self.visit(condition, context))
            if res.error: return res

            if condition_value.is_true():
                expr_value = res.register(self.visit(expr, context))
                if res.error: return res
                return res.success(expr_value)

        if node.else_case:
            else_value = res.register(self.visit(node.else_case, context))
            if res.error: return res
            return res.success(else_value)

        return res.success(None)

    ###############################
    # FOR NODE VISIT METHOD 
    ###############################
    def visit_ForNode(self, node, context):
        res = RTResult()
        elements = []

        start_value = res.register(self.visit(node.start_value_node, context))
        if res.error: return res

        end_value = res.register(self.visit(node.end_value_node, context))
        if res.error: return res

        if node.step_value_node:
            step_value = res.register(self.visit(node.step_value_node, context))
            if res.error: return res
        else:
            step_value = Number(1)

        i = start_value.value

        if step_value.value >= 0:
            condition = lambda: i < end_value.value
        else:
            condition = lambda: i > end_value.value

        while condition():
            context.symbol_table.set(node.var_name_tok.value, Number(i))
            i += step_value.value

            elements.append(res.register(self.visit(node.body_node, context)))
            if res.error: return res

        return res.success(
            List(elements).set_context(context).set_pos(node.pos_start, node.pos_end)
            )

    ###############################
    # WHILE NODE VISIT METHOD 
    ###############################
    def visit_WhileNode(self, node, context):
        res = RTResult()
        elements = []

        while True:
            condition = res.register(self.visit(node.condition_node, context))
            if res.error: return res

            if not condition.is_true(): break

            elements.append(res.register(self.visit(node.body_node, context)))
            if res.error: return res

        
        return res.success(
            List(elements).set_context(context).set_pos(node.pos_start, node.pos_end)
            )

    def visit_FuncDefNode(self, node, context):
        res = RTResult()

        func_name = node.var_name_tok.value if node.var_name_tok else None
        body_node = node.body_node
        arg_names = [arg_name.value for arg_name in node.arg_name_toks]
        func_value = Function(func_name, body_node, arg_names).set_context(context).set_pos(node.pos_start, node.pos_end)
        
        if node.var_name_tok:
            context.symbol_table.set(func_name, func_value)

        return res.success(func_value)

    def visit_CallNode(self, node, context):
        res = RTResult()
        args = []

        value_to_call = res.register(self.visit(node.node_to_call, context))
        if res.error: return res
        value_to_call = value_to_call.copy().set_pos(node.pos_start, node.pos_end)

        for arg_node in node.arg_nodes:
            args.append(res.register(self.visit(arg_node, context)))
            if res.error: return res

        return_value = res.register(value_to_call.execute(args))
        if res.error: return res
        return_value = return_value.copy().set_context(context).set_pos(node.pos_start,node.pos_end)
        return res.success(return_value)

###################################################
# RUN                      - usain bolt un poroto -
###################################################

global_symbol_table = SymbolTable()
global_symbol_table.set("Milanesa",String("Carne"))
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
    context = Context("<program>")
    context.symbol_table = global_symbol_table
    result = interpreter.visit(ast.node, context)

    return result.value, result.error