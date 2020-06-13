from stringsWithArrows import * # eto pone flechitas en los errore
import string
import random
###################################################
# CONSTANTS - me dijeron que significa constantes -
###################################################

DIGITS = "0123456789" # los numerito
LETTERS = string.ascii_letters
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
detailsMessages = {
    "intOrFloatExpected" : "\nFlaco pasame un numerito ahi viste",
    "exprExpected" : "\nFlaco pasame un algo ahi viste",
    "operationExpected": "\nFlaco dame alguna operacion, lamentablemente no puedo hacer lo que me pinte",
    "closeParentesisExpected": "\nFlaco porque no cerras los partentesis?",
    "identifierExpected": "\nDecime un nombre pa la variable viste",
    "equalExpected": "\nTenes que poner 'es' pa poner algo crack",
    "equalAfterNotExpected": "\nChe no sabes español? Tenes que poner 'No es'",
    "zeroDiv": "\ndividís por cero vos? Usted se tiene que arrepentir de lo que dijo",
    "unknownVariable": "\nCapo no me dijiste que es '",
    "languajeSyntaxError": "\nGenio leete la doc antes de escribir dale? Te faltó algo"
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
        result += f"En {self.pos_start.fn}, linea {self.pos_start.ln + 1} o por ahí" #era re croto viste
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
# RUNTIME ERROR
###############################
class RTError(Error):
    def __init__(self, pos_start, pos_end, details, context):
        super().__init__(pos_start, pos_end, errorMessages["RuntimeError"], details)
        self.context = context

    def as_string(self):
        result = self.generate_traceback()
        result += f"{self.error_name}: {self.details} \n"
        result += "\n\n" + string_with_arrows(self.pos_start.ftxt, self.pos_start, self.pos_end)
        return result

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
TT_EE = "EE"
TT_MM = "MM"
TT_NE = "NE"
TT_LT = "LT"
TT_GT = "GT"
TT_LTE = "LTE"
TT_GTE = "GTE"
TT_EOF = "EOF"

KEYWORDS = [
    "che",
    "y",
    "o",
    "no",
    "ponele",
    "tonce",
    "osi",
    "alosumo"
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
                tokens.append(self.make_number())
            elif self.current_char in LETTERS + "()":
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

        if dot_count == 0:
            return Token(TT_INT, int(num_str), pos_start, self.pos)
        else:
            return Token(TT_FLOAT, float(num_str), pos_start, self.pos)

    
    ###############################
    # OPERATOR FACTORY      ¡op op!
    ###############################

    def make_operator(self, next_str=None):
        op_str = ""
        pos_start = self.pos.copy()

        if next_str == None:
            while self.current_char != None and self.current_char in LETTERS + "()":
                op_str += self.current_char
                self.advance()
        else: op_str = next_str

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
        elif op_str.lower() == "(":
            return [Token(TT_LPAREN, pos_start=pos_start, pos_end=self.pos)] , None
        elif op_str.lower() == ")":
            return [Token(TT_RPAREN, pos_start=pos_start, pos_end=self.pos)] , None
        elif op_str.lower() == "anda":
            if self.take_str().lower() == "por":
                return [Token(TT_EE, pos_start=pos_start, pos_end=self.pos)] , None
            else: return [], InvalidSyntaxError(
                pos_start, self.pos,
                detailsMessages["languajeSyntaxError"]
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
                    detailsMessages["languajeSyntaxError"]
                    )
            return [Token(tok_type, op_str, pos_start, self.pos)], None

    def make_not_equals(self):
        pos_start = self.pos.copy()
        ne_str = self.take_str()
        
        if ne_str.lower() == "es":
            return [Token(TT_NE, pos_start=pos_start, pos_end=self.pos)], None
        
        return None, ExpectedCharError(pos_start,self.pos,detailsMessages["equalAfterNotExpected"])

    def take_str(self):
        new_str = ""
        self.advance()

        while self.current_char != None and self.current_char in LETTERS + "()":
            new_str += self.current_char
            self.advance()

        return new_str

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
# UNARYOPERATIONS  - los meno -
###############################
class UnaryOpNode:
    def __init__(self, op_tok, node):
        self.op_tok = op_tok
        self.node = node
    
        self.pos_start = self.op_tok.pos_start
        self.pos_end = self.node.pos_end

    def __repr__(self):
        return f"({self.op_tok}, {self.node})"

class IfNode:
    def __init__(self, cases, else_case):
        self.cases = cases
        self.else_case = else_case

        self.pos_start = self.cases[0][0].pos_start
        self.pos_end = self.else_case or self.cases[-1][0].pos_end

###################################################
# PARSE RESULT   - ete se fija si hiciste macanas -
###################################################
class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None
        self.advance_count = 0

    def register_advancement(self):
        self.advance_count += 1

    def register(self, res):
        self.advance_count += res.advance_count
        if res.error: self.error = res.error
        return res.node

    ###############################
    # SUCCESS METHOD     ganadorr -
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
    # FACTOR METHOD - so numerito -
    ###############################
    def atom(self):
        res = ParseResult()
        tok = self.current_tok

        if tok.type in (TT_INT, TT_FLOAT):
            res.register_advancement()
            self.advance()
            return res.success(NumberNode(tok))

        elif tok.type == TT_IDENTIFIER:
            res.register_advancement()
            self.advance()
            return res.success(VarAccessNode(tok))

        elif tok.type == TT_LPAREN:# si tiene un parentesi le da las prioridade
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
        
        elif tok.matches(TT_KEYWORD, "ponele"):
            if_expr = res.register(self.if_expr())
            if res.error: return res
            return res.success(if_expr)

        return res.failure(InvalidSyntaxError(
            tok.pos_start, tok.pos_end,
            detailsMessages["intOrFloatExpected"]
        ))

    def power(self):
        return self.bin_op(self.atom, (TT_POW, ), self.factor)

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

    def if_expr(self):
        res = ParseResult()
        cases = []
        else_case = None

        if not self.current_tok.matches(TT_KEYWORD, "ponele"):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "if expected"
            ))
        
        res.register_advancement()
        self.advance()

        condition = res.register(self.expr())
        if res.error:return res

        if not self.current_tok.matches(TT_KEYWORD, "tonce"):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "then expected"
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
                    "then expected"
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

    def register(self, res):
        if res.error: self.error = res.error
        return res.value

    def success(self, value):
        self.value = value
        return self

    def failure(self, error):
        self. error = error
        return self


###################################################
# VALUES
###################################################

class Number:
    def __init__(self,value):
        self.value = value
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
        if isinstance(other, Number):
            return Number(self.value + other.value).set_context(self.context), None

    def subbed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value).set_context(self.context), None

    def multed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value).set_context(self.context), None

    def dived_by(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, RTError(
                    other.pos_start, other.pos_end,
                    detailsMessages["zeroDiv"],
                    self.context
                )
            else:
                return Number(self.value / other.value).set_context(self.context), None

    def powed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value ** other.value).set_context(self.context), None

    def get_comparison_ee(self,other):
        if isinstance(other,Number):
            return Number(int(self.value == other.value)).set_context(self.context), None
    
    def get_comparison_ne(self,other):
        if isinstance(other,Number):
            return Number(int(self.value != other.value)).set_context(self.context), None
    
    def get_comparison_lt(self,other):
        if isinstance(other,Number):
            return Number(int(self.value < other.value)).set_context(self.context), None
    
    def get_comparison_gt(self,other):
        if isinstance(other,Number):
            return Number(int(self.value > other.value)).set_context(self.context), None
    
    def get_comparison_lte(self,other):
        if isinstance(other,Number):
            return Number(int(self.value <= other.value)).set_context(self.context), None
    
    def get_comparison_gte(self,other):
        if isinstance(other,Number):
            return Number(int(self.value >= other.value)).set_context(self.context), None
    
    def get_comparison_mm(self,other):
        if isinstance(other,Number):
            if self.value >= other.value - other.value * .20 and self.value <= other.value + other.value * .20:
                return Number(1).set_context(self.context), None
            elif other.value >= self.value - self.value * .20 and other.value <= self.value + self.value * .20:
                return Number(1).set_context(self.context), None
            else:
                return Number(0).set_context(self.context), None

    def anded_by(self, other):
        if isinstance(other, Number):
            return Number(int(self.value and other.value)).set_context(self.context), None

    def ored_by(self, other):
        if isinstance(other, Number):
            return Number(int(self.value or other.value)).set_context(self.context), None

    def notted(self):
        return Number(1 if self.value == 0 else 0).set_context(self.context), None

    def is_true(self):
        return self.value != 0

    def copy(self):
        copy = Number(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def __repr__(self):
        return str(self.value)

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
    def __init__(self):
        self.symbols = {}
        self.parent = None

    def get(self, name):
        value = self.symbols.get(name, None)
        if value == None and self.parent:
            return self.parent.get(name)
        return value

    def set(self, name, value):
        self.symbols[name] = value

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

    def no_visit_method(self, node, context):
        raise Exception(f"No visit_{type(node).__name__} method defined")

    def visit_NumberNode(self, node, context):
        return RTResult().success(
            Number(node.tok.value).set_context(context).set_pos(node.pos_start,node.pos_end)
        )

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

        value = value.copy().set_pos(node.pos_start, node.pos_end)
        return res.success(value)

    def visit_VarAssignNode(self, node, context):
        res = RTResult()
        var_name = node.var_name_tok.value
        value = res.register(self.visit(node.value_node, context))
        if res.error: return res

        context.symbol_table.set(var_name,value)
        return res.success(value)

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


###################################################
# RUN                      - usain bolt un poroto -
###################################################

global_symbol_table = SymbolTable()
global_symbol_table.set("inviable",Number(0))
global_symbol_table.set("posta",Number(1))
global_symbol_table.set("chamuyo",Number(0))
global_symbol_table.set("milanesa","carne")

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