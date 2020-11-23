from CheLang.Position import Position
from CheLang.Const import detailsMessages, LETTERS, DIGITS, TT_LPAREN, TT_RPAREN, TT_LSQUARE, TT_RSQUARE, TT_COMMA, TT_ARROW, TT_EOF, TT_INT, TT_FLOAT, TT_PLUS, TT_MINUS, TT_MOD, TT_MUL, TT_DIV, TT_POW, TT_EE, TT_EQ, TT_KEYWORD, KEYWORDS, TT_IDENTIFIER, TT_STRING, TT_NE, TT_LT, TT_LTE, TT_GT, TT_GTE, TT_MM, TT_NEWLINE
from CheLang.Tokens import Token
from CheLang.Errors import InvalidSyntaxError, IllegalCharError, ExpectedCharError
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
        # aca se fija que onda con lo que tiene
        while self.current_char != None:
            if self.current_char in " \t":
                self.advance()
            if self.current_char == "#":
                self.skip_comment()
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
            elif self.current_char in ";\n":
                tokens.append(Token(TT_NEWLINE, pos_start=self.pos))
                self.advance()
            elif self.current_char == "[":
                tokens.append(Token(TT_LSQUARE, pos_start=self.pos, pos_end=self.pos))
                self.advance()
            elif self.current_char == "]":
                tokens.append(Token(TT_RSQUARE, pos_start=self.pos, pos_end=self.pos))
                self.advance()
            elif self.current_char == "%":
                tokens.append(Token(TT_MOD, pos_start=self.pos, pos_end=self.pos))
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
                char = self.current_char 
                if char != " ":
                    pos_start = self.pos.copy()
                    self.advance()
                    return [], IllegalCharError(pos_start, self.pos, char) #pa los que no saben escribir
                else:
                    self.advance()
        # end of file, lo que va al final vite
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
        elif op_str.lower() == "moduleame":
            return [Token(TT_MOD, pos_start=pos_start, pos_end=self.pos)] , None
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
        elif op_str.lower() == "son":
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
            # esto se fija las keywords que tienen mas de una palabra
            if op_str.lower() == "ponele":
                if self.take_str().lower() != "que": return [], InvalidSyntaxError(
                    pos_start, self.pos,
                    detailsMessages["languajeSyntaxError"] + "que'"
                    )
            elif op_str.lower() == "digamos":
                if self.take_str().lower() != "que": return [], InvalidSyntaxError(
                    pos_start, self.pos,
                    detailsMessages["languajeSyntaxError"] + "que'"
                    )
            elif op_str.lower() == "agarra":
                if self.take_str().lower() != "por": return [], InvalidSyntaxError(
                    pos_start, self.pos,
                    detailsMessages["languajeSyntaxError"] + "por'"
                    )
            elif op_str.lower() == "de":
                if self.take_str().lower() != "a": return [], InvalidSyntaxError(
                    pos_start, self.pos,
                    detailsMessages["languajeSyntaxError"] + "a'"
                    )
            elif op_str.lower() == "segui":
                if self.take_str().lower() != "de": return [], InvalidSyntaxError(
                    pos_start, self.pos,
                    detailsMessages["languajeSyntaxError"] + "segui de largo'"
                    )
                if self.take_str().lower() != "largo": return [], InvalidSyntaxError(
                    pos_start, self.pos,
                    detailsMessages["languajeSyntaxError"] + "segui de largo'"
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
        # la cosa es agarrar la proxima palabra
        while self.current_char != None and self.current_char in LETTERS:
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
    ###############################
    # COMMENT - haha recursiv goes brr - 
    ###############################
    def skip_comment(self):
        while self.current_char != "\n" and self.current_char != None:
            self.advance()
