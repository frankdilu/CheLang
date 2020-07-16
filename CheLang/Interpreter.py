from CheLang.Values import Value,List, String, Number, Function, Empty
from CheLang.Const import detailsMessages, TT_PLUS, TT_MINUS, TT_MOD, TT_MUL, TT_DIV, TT_POW, TT_EE,TT_NE, TT_LT,TT_GT,TT_LTE,TT_GTE,TT_MM,TT_KEYWORD
from CheLang.RTResult import RTResult
from CheLang.Errors import RTError, LanguageThingError
###################################################
# INTERPRETER
###################################################

class Interpreter:
    ###############################
    # VISIT METHOD
    ###############################
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
    ###############################
    # STRING VISIT METHOD 
    ###############################
    def visit_StringNode(self, node, context):
        return RTResult().success(
            String(node.tok.value).set_context(context).set_pos(node.pos_start, node.pos_end)
        )
    ###############################
    # LIST VISIT METHOD 
    ###############################
    def visit_ListNode(self, node, context):
        res = RTResult()
        elements = []

        for element_node in node.element_nodes:
            elements.append(res.register(self.visit(element_node, context)))
            # if res.error: return res
            if res.should_return(): return res

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
        var_name = node.var_name_tok
        value = res.register(self.visit(node.value_node, context))
        # if res.error: return res
        if res.should_return(): return res
        for var in var_name:
            if var.value.lower() == "dolar":
                return res.failure(LanguageThingError(
                        var.pos_start, var.pos_end,
                        detailsMessages["dolarVarAssign"]
                        ))
            context.symbol_table.set(var.value,value)
        return res.success(value)

    ###############################
    # BIN OP VISIT METHOD 
    ###############################
    def visit_BinOpNode(self, node, context):
        res = RTResult()
        left = res.register(self.visit(node.left_node, context))
        # if res.error: return res
        if res.should_return(): return res
        right = res.register(self.visit(node.right_node, context))
        # if res.error: return res
        if res.should_return(): return res

        if node.op_tok.type == TT_PLUS:
            result, error = left.added_to(right)
        elif node.op_tok.type == TT_MINUS:
            result, error = left.subbed_by(right)
        elif node.op_tok.type == TT_MUL:
            result, error = left.multed_by(right)
        elif node.op_tok.type == TT_MOD:
            result, error = left.modded_by(right)
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
        # if res.error: return res
        if res.should_return(): return res

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

        for condition, expr, should_return_null in node.cases:
            condition_value = res.register(self.visit(condition, context))
            # if res.error: return res
            if res.should_return(): return res

            if condition_value.is_true():
                expr_value = res.register(self.visit(expr, context))
                # if res.error: return res
                if res.should_return(): return res
                return res.success(Empty() if should_return_null else expr_value)

        if node.else_case:
            expr, should_return_null = node.else_case
            else_value = res.register(self.visit(expr, context))
            # if res.error: return res
            if res.should_return(): return res
            return res.success(Empty() if should_return_null else else_value)

        return res.success(Empty())

    ###############################
    # FOR NODE VISIT METHOD 
    ###############################
    def visit_ForNode(self, node, context):
        res = RTResult()
        elements = []

        start_value = res.register(self.visit(node.start_value_node, context))
        # if res.error: return res
        if res.should_return(): return res

        end_value = res.register(self.visit(node.end_value_node, context))
        # if res.error: return res
        if res.should_return(): return res

        if node.step_value_node:
            step_value = res.register(self.visit(node.step_value_node, context))
            # if res.error: return res
            if res.should_return(): return res
        else:
            step_value = Number(1)

        i = start_value.value

        if step_value.value >= 0:
            condition = lambda: i < end_value.value
        else:
            condition = lambda: i > end_value.value
        # aca ta el loop
        while condition():
            context.symbol_table.set(node.var_name_tok.value, Number(i))
            i += step_value.value

            value = res.register(self.visit(node.body_node, context))
            # if res.error: return res
            if res.should_return() and res.loop_should_continue == False and res.loop_should_break == False: return res

            if res.loop_should_continue:
                continue

            if res.loop_should_break:
                break
            if type(value) != Empty:
                elements.append(value)

        return res.success(
            Empty() if node.should_return_null else
            List(elements).set_context(context).set_pos(node.pos_start, node.pos_end)
            )

    ###############################
    # WHILE NODE VISIT METHOD 
    ###############################
    def visit_WhileNode(self, node, context):
        res = RTResult()
        elements = []
        # aca ta el loop
        while True:
            condition = res.register(self.visit(node.condition_node, context))
            # if res.error: return res
            if res.should_return(): return res

            if not condition.is_true(): break

            value = res.register(self.visit(node.body_node, context))
            # if res.error: return res
            if res.should_return()  and res.loop_should_continue == False and res.loop_should_break == False: return res

            if res.loop_should_continue:
                continue
            if res.loop_should_break:
                break

            elements.append(value)
        
        return res.success(
            Empty() if node.should_return_null else
            List(elements).set_context(context).set_pos(node.pos_start, node.pos_end)
            )
    ###############################
    # FUNC DEF VISIT METHOD 
    ###############################
    def visit_FuncDefNode(self, node, context):
        res = RTResult()

        func_name = node.var_name_tok.value if node.var_name_tok else None
        body_node = node.body_node
        arg_names = [arg_name.value for arg_name in node.arg_name_toks]
        func_value = Function(func_name, body_node, arg_names, node.should_auto_return).set_context(context).set_pos(node.pos_start, node.pos_end)
        
        if node.var_name_tok:
            context.symbol_table.set(func_name, func_value)

        return res.success(func_value)
    ###############################
    # LIST CALL VISIT METHOD 
    ###############################
    def visit_CallListNode(self, node, context):
        res = RTResult()

        value_to_call = res.register(self.visit(node.list_to_call, context))
        if res.should_return(): return res
        value_to_call = value_to_call.copy().set_pos(node.pos_start, node.pos_end)

        listIndex = res.register(self.visit(node.listIndex, context))
        if res.should_return(): return res
        listIndex = listIndex.copy().set_pos(node.pos_start, node.pos_end)

        return_value = res.register(value_to_call.take_item(listIndex))
        if res.should_return(): return res
        return_value = return_value.copy().set_context(context).set_pos(node.pos_start,node.pos_end)
        return res.success(return_value)
    ###############################
    # FUN CALL VISIT METHOD 
    ###############################
    def visit_CallNode(self, node, context):
        res = RTResult()
        args = []

        value_to_call = res.register(self.visit(node.node_to_call, context))
        if res.should_return(): return res
        value_to_call = value_to_call.copy().set_pos(node.pos_start, node.pos_end)

        for arg_node in node.arg_nodes:
            args.append(res.register(self.visit(arg_node, context)))
            if res.should_return(): return res

        return_value = res.register(value_to_call.execute(args))
        if res.should_return(): return res
        return_value = return_value.copy().set_context(context).set_pos(node.pos_start,node.pos_end)
        return res.success(return_value)
    ###############################
    # RETURN VISIT METHOD 
    ###############################
    def visit_ReturnNode(self, node, context):
        res = RTResult()

        if node.node_to_return:
            value = res.register(self.visit(node.node_to_return, context))
            if res.should_return() : return res
        else:
            value = Number.null

        return res.success_return(value)
    ###############################
    # CONTINUE VISIT METHOD 
    ###############################
    def visit_ContinueNode(self, node, context):
        return RTResult().success_continue()
    ###############################
    # BREAK VISIT METHOD 
    ###############################
    def visit_BreakNode(self, node, context):
        return RTResult().success_break()