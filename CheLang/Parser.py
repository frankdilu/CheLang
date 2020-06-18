from CheLang.Const import TT_EOF,TT_POW, TT_LPAREN, TT_RPAREN, TT_COMMA, TT_INT, TT_FLOAT, TT_STRING, TT_IDENTIFIER, TT_LSQUARE, TT_KEYWORD, TT_PLUS, TT_MINUS, TT_MUL, TT_DIV, TT_RSQUARE, TT_EQ, TT_EE, TT_NE, TT_LT, TT_GT, TT_LTE, TT_GTE, TT_MM, TT_ARROW, TT_NEWLINE
from CheLang.Errors import InvalidSyntaxError, detailsMessages
from CheLang.ParserResult import ParseResult
from CheLang.Nodes import CallNode, NumberNode, StringNode, VarAccessNode, UnaryOpNode, ListNode, IfNode, ForNode, WhileNode, VarAssignNode, FuncDefNode, BinOpNode, ReturnNode, ContinueNode, BreakNode

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
        self.update_current_tok()
        return self.current_tok

    ###############################
    # REVERSE METHOD    - pa atra -
    ###############################
    def reverse(self, amount=1):
        self.tok_inx -= amount
        self.update_current_tok()
        return self.current_tok

    ###############################
    # UPDATE TOK METHOD
    ###############################
    def update_current_tok(self):
        if self.tok_inx >= 0 and self.tok_inx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_inx]


    ###############################
    # PARSE METHOD
    ###############################
    def parse(self):
        res = self.statements()
        if not res.error and self.current_tok.type != TT_EOF:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                detailsMessages["exprExpected"]
            ))
        return res

    ###############################
    # STATEMENTS    mas de una expr
    ###############################
    def statements(self):
        res = ParseResult()
        statements = []
        pos_start = self.current_tok.pos_start.copy()

        while self.current_tok.type == TT_NEWLINE:
            res.register_advancement()
            self.advance()

        statement = res.register(self.statement())
        if res.error: return res
        statements.append(statement)

        more_statements = True

        while True:
            newline_count = 0
            while self.current_tok.type == TT_NEWLINE:
                res.register_advancement()
                self.advance()
                newline_count += 1
            if newline_count == 0:
                more_statements = False
            
            if not more_statements: break
            statement = res.try_register(self.statement())
            if not statement:
                self.reverse(res.to_reverse_count)
                more_statements = False
                continue
            statements.append(statement)

        return res.success(ListNode(
            statements,
            pos_start,
            self.current_tok.pos_end.copy()
            ))

    ###############################
    # POWER METHOD - qué potente. -
    ###############################
    def power(self):
        return self.bin_op(self.call, (TT_POW, ), self.factor)

    ###############################
    # CALL METHOD       - atomiza -
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
                        detailsMessages["exprExpected"]
                    ))

                while self.current_tok.type == TT_COMMA:
                    res.register_advancement()
                    self.advance()

                    arg_nodes.append(res.register(self.expr()))
                    if res.error: return res

                if self.current_tok.type != TT_RPAREN:
                    return res.failure(InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        detailsMessages["languajeSyntaxError"] + ")' o ','"
                    ))

                res.register_advancement()
                self.advance()
            return res.success(CallNode(atom, arg_nodes))
        return res.success(atom)


    ###############################
    # ATOM METHOD        - que so -
    ###############################
    def atom(self):
        res = ParseResult()
        tok = self.current_tok
        # Che, es un numerin?
        if tok.type in (TT_INT, TT_FLOAT):
            res.register_advancement()
            self.advance()
            return res.success(NumberNode(tok))
        # Che, es un estrin?
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
        elif tok.matches(TT_KEYWORD, "agarra"):
            for_expr = res.register(self.for_expr())
            if res.error: return res
            return res.success(for_expr)

        # Che, es un while?
        elif tok.matches(TT_KEYWORD, "mientras"):
            while_expr = res.register(self.while_expr())
            if res.error: return res
            return res.success(while_expr)
        
        # Che, es una funcion?
        elif tok.matches(TT_KEYWORD, "definime"):
            func_def = res.register(self.func_def())
            if res.error: return res
            return res.success(func_def)

        # Che, es una niu lain?
        elif tok.type == TT_NEWLINE:
            self.advance()
            statement = res.register(self.statement())
            if res.error: return res
            return res.success(statement)

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
    # ARITH METHOD       - que so -
    ###############################
    def arith_expr(self):
        return self.bin_op(self.term,(TT_PLUS, TT_MINUS))

    ###############################
    # LIST EXPR METHOD - la lista -
    ###############################
    def list_expr(self):
        res = ParseResult()
        element_nodes = []
        pos_start = self.current_tok.pos_start.copy()

        if self.current_tok.type != TT_LSQUARE:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                detailsMessages["languajeSyntaxError"] + "['"
            ))

        res.register_advancement()
        self.advance()
        # si cierra el corchet termina las cuestione
        if self.current_tok.type == TT_RSQUARE:
            res.register_advancement()
            self.advance()
        # si no lo cierra las sigue
        else:
            element_nodes.append(res.register(self.expr()))
            if res.error:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    detailsMessages["exprExpected"]
                ))

            while self.current_tok.type == TT_COMMA:
                res.register_advancement()
                self.advance()

                element_nodes.append(res.register(self.expr()))
                if res.error: return res
            #si tiene mas de una cuestion y no cierra el corchet tamo complicado
            if self.current_tok.type != TT_RSQUARE:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    detailsMessages["languajeSyntaxError"] + ")' o ','"
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
        all_cases = res.register(self.if_expr_cases('ponele'))
        if res.error: return res
        cases, else_case = all_cases
        return res.success(IfNode(cases, else_case))
    # Che, es elif?
    def if_expr_b(self):
        return self.if_expr_cases('osi')
    # o es else?
    def if_expr_c(self):
        res = ParseResult()
        else_case = None
        # si tenemo un else hacemo eto
        if self.current_tok.matches(TT_KEYWORD, 'alosumo'):
            res.register_advancement()
            self.advance()

            if self.current_tok.type == TT_NEWLINE:
                res.register_advancement()
                self.advance()

                statements = res.register(self.statements())
                if res.error: return res
                else_case = (statements, True)

                if self.current_tok.matches(TT_KEYWORD, 'hastaaca'):
                    res.register_advancement()
                    self.advance()
                else:
                    return res.failure(InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        detailsMessages["languajeSyntaxError"] + "hastaaca'"
                        ))
            else:
                expr = res.register(self.statement())
                if res.error: return res
                else_case = (expr, False)
        # si no tenemo else le mandamo al none
        return res.success(else_case)

    # si tiene un elif le manda al elif, si tiene el elsé le manda al elsé
    def if_expr_b_or_c(self):
        res = ParseResult()
        cases, else_case = [], None

        if self.current_tok.matches(TT_KEYWORD, 'osi'):
            all_cases = res.register(self.if_expr_b())
            if res.error: return res
            cases, else_case = all_cases
        else:
            else_case = res.register(self.if_expr_c())
            if res.error: return res
        
        return res.success((cases, else_case))

    # esto es pa los ife y pa los elife, le pasa la keyword
    # y hace las cuestiones dependiendo de eso
    def if_expr_cases(self, case_keyword):
        res = ParseResult()
        cases = []
        else_case = None

        if not self.current_tok.matches(TT_KEYWORD, case_keyword):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                detailsMessages["languajeSyntaxError"] + case_keyword + "'"
                ))

        res.register_advancement()
        self.advance()

        condition = res.register(self.expr())
        if res.error: return res

        if not self.current_tok.matches(TT_KEYWORD, 'tonce'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                detailsMessages["languajeSyntaxError"] + "tonce'"
                ))

        res.register_advancement()
        self.advance()

        if self.current_tok.type == TT_NEWLINE:
            res.register_advancement()
            self.advance()

            statements = res.register(self.statements())
            if res.error: return res
            cases.append((condition, statements, True))

            if self.current_tok.matches(TT_KEYWORD, 'hastaaca'):
                res.register_advancement()
                self.advance()
            else:
                all_cases = res.register(self.if_expr_b_or_c())
                if res.error: return res
                new_cases, else_case = all_cases
                cases.extend(new_cases)
        else:
            expr = res.register(self.statement())
            if res.error: return res
            cases.append((condition, expr, False))

            all_cases = res.register(self.if_expr_b_or_c())
            if res.error: return res
            new_cases, else_case = all_cases
            cases.extend(new_cases)

        return res.success((cases, else_case))


    ###############################
    # FOR METHOD     - da vueltas -
    ###############################
    def for_expr(self):
        res = ParseResult()

        if not self.current_tok.matches(TT_KEYWORD, "agarra"):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                detailsMessages["languajeSyntaxError"] + "agarra'"
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

        if not self.current_tok.matches(TT_KEYWORD, "hasta"):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                detailsMessages["languajeSyntaxError"] + "to'"
            ))

        res.register_advancement()
        self.advance()

        end_value = res.register(self.expr())
        if res.error: return res

        if self.current_tok.matches(TT_KEYWORD, "de"):
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

        if self.current_tok.type == TT_NEWLINE:
            res.register_advancement()
            self.advance()
            
            body = res.register(self.statements())
            if res.error: return res

            if not self.current_tok.matches(TT_KEYWORD, "hastaaca"):
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    detailsMessages["languajeSyntaxError"] + "hastaaca'"
                ))

            res.register_advancement()
            self.advance()

            return res.success(ForNode(var_name, start_value, end_value, step_value, body, True))
            

        body = res.register(self.statement())
        if res.error: return res

        return res.success(ForNode(var_name, start_value, end_value, step_value, body, False))

    ###############################
    # WHILE METHOD - da vueltitas -
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

        
        if self.current_tok.type == TT_NEWLINE:
            res.register_advancement()
            self.advance()
            
            body = res.register(self.statements())
            if res.error: return res

            if not self.current_tok.matches(TT_KEYWORD, "hastaaca"):
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    detailsMessages["languajeSyntaxError"] + "hastaaca'"
                ))

            res.register_advancement()
            self.advance()
            return res.success(WhileNode(condition, body, True))


        body = res.register(self.statement())
        if res.error: return res
        
        return res.success(WhileNode(condition, body, False))

    ###############################
    # COMPARATOR METHOD  - iguale -
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
    # si tiene un return o break o continue rompe todo,
    # sino le manda a las cuestione
    def statement(self):
        res = ParseResult()
        pos_start = self.current_tok.pos_start.copy()

        if self.current_tok.matches(TT_KEYWORD, 'tirame'):
            res.register_advancement()
            self.advance()

            expr = res.try_register(self.expr())
            if not expr:
                self.reverse(res.to_reverse_count)
            return res.success(ReturnNode(expr, pos_start, self.current_tok.pos_start.copy()))
        
        if self.current_tok.matches(TT_KEYWORD, 'segui'):
            res.register_advancement()
            self.advance()
            return res.success(ContinueNode(pos_start, self.current_tok.pos_start.copy()))
        if self.current_tok.matches(TT_KEYWORD, 'piquete'):
            res.register_advancement()
            self.advance()
            return res.success(BreakNode(pos_start, self.current_tok.pos_start.copy()))


        expr = res.register(self.expr())
        if res.error:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                detailsMessages["exprExpected"]
                ))
        return res.success(expr)

    ###############################
    # EXPR METHOD - las cuestione -
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
        # si no le pones la keyword de funcion tamo complicado
        if not self.current_tok.matches(TT_KEYWORD, 'definime'):
            return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    detailsMessages["languajeSyntaxError"] + "FUN'"
                    ))

        res.register_advancement()
        self.advance()
        # si tiene nombre le hace un dni con su nombre
        if self.current_tok.type == TT_IDENTIFIER:
            var_name_tok = self.current_tok
            res.register_advancement()
            self.advance()
            if self.current_tok.type != TT_LPAREN:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    detailsMessages["languajeSyntaxError"] + "('"
                ))
        # si no tiene nombre la hace anonimu' ah re jakier
        else:
            var_name_tok = None
            if self.current_tok.type != TT_LPAREN:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    detailsMessages["languajeSyntaxError"] + "('"
                ))
        
        res.register_advancement()
        self.advance()
        arg_name_toks = []
        # aca agarra los argumento. si tiene un identifaier le manda fruta y sino no duh
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
                        detailsMessages["languajeSyntaxError"] + "nombre de variable'"
                    ))

                arg_name_toks.append(self.current_tok)
                res.register_advancement()
                self.advance()
            
            if self.current_tok.type != TT_RPAREN:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    detailsMessages["languajeSyntaxError"] + ",' o ')'"
                ))
        # si no tiene identifaier osea que no tiene argumentos
        # se fija si cierra parentesis. si no lo cierra rompe todo
        else:
            if self.current_tok.type != TT_RPAREN:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    detailsMessages["languajeSyntaxError"] + "nombre de variable' o ')'"
                ))

        res.register_advancement()
        self.advance()
        # si tiene arrow se fija por una cuestion sola
        if self.current_tok.type == TT_ARROW:
            res.register_advancement()
            self.advance()
            body = res.register(self.expr())
            if res.error: return res

            return res.success(FuncDefNode(
                var_name_tok,
                arg_name_toks,
                body,
                True
            ))

        # si no tiene arrow tiene que tener una niu lain
        if self.current_tok.type != TT_NEWLINE:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                detailsMessages["languajeSyntaxError"] + "=>' o nueva linea (\\n)"
            ))
        #si tiene niu lain le manda hasta un hastaaca we re claro era el tipo
        res.register_advancement()
        self.advance()

        body = res.register(self.statements())
        if res.error: return res
        # y si no tiene un hastaaca rompe todo... 
        # Me estoy dando cuenta que rompe todo en cualquier momento
        if not self.current_tok.matches(TT_KEYWORD, "hastaaca"):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                detailsMessages["languajeSyntaxError"] + "hastaaca'"
            ))
        res.register_advancement()
        self.advance()

        return res.success(FuncDefNode(
            var_name_tok,
            arg_name_toks,
            body,
            False
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
