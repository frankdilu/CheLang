from CheLang.RTResult import RTResult
from CheLang.Errors import RTError
from CheLang.Const import detailsMessages
import math
from CheLang.Context import Context
from CheLang.SymbolTable import SymbolTable
import os
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
        raise Exception('No hay copy() acá master')

    def is_true(self):
        return False

    def illegal_operation(self, other=None):
        if not other: other = self
        return RTError(
            self.pos_start, other.pos_end,
            'Wait... that´s illegal',
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
                    detailsMessages["zeroDiv"],
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

class Empty(Value):
    def __init__(self):
        super().__init__()

    def copy(self):
        return Empty()

    def __repr__(self):
        return "Vacio a la parrilla"

    def __str__(self):
        return "Vacio a la parrilla"

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

    def get_comparison_ee(self, other):
        if isinstance(other, String):
            return Number(int(self.value == other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

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
                    detailsMessages["outOfIndex"],
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
                    detailsMessages["outOfIndex"],
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
        final_arg_names = []

        for arg_name in arg_names:
            if not arg_name[-1] == "?":
                final_arg_names.append(arg_name)

        if len(args) > len(arg_names):
            return res.failure(RTError(
                self.pos_start, self.pos_end,
                f"Che me pasaste como {len(args) - len(arg_names)} argumentos, son menos en {self} viste",
                self.context
            ))
        
        if len(args) < len(final_arg_names):
            return res.failure(RTError(
                self.pos_start, self.pos_end,
                f"Che me pasaste como {len(final_arg_names) - len(args)} argumentos, son más en {self} viste",
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
        if res.should_return(): return res
        self.populate_args(arg_names, args, exec_ctx)
        return res.success(None)

class Function(BaseFunction):
    def __init__(self, name, body_node, arg_names, should_auto_return):
        super().__init__(name)
        self.body_node = body_node
        self.arg_names = arg_names
        self.should_auto_return = should_auto_return

    def execute(self, args):
        from CheLang.Interpreter import Interpreter
        res = RTResult()
        interpreter = Interpreter()
        exec_ctx = self.generate_new_context()

        res.register(self.check_and_populate_args(self.arg_names, args, exec_ctx))
        if res.should_return(): return res

        value = res.register(interpreter.visit(self.body_node, exec_ctx))
        if res.should_return() and res.func_return_value == None: return res
        
        ret_value = (value if self.should_auto_return else None) or res.func_return_value or Empty()
        return res.success(ret_value)

    def copy(self):
        copy = Function(self.name, self.body_node, self.arg_names, self.should_auto_return)
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
        if res.should_return(): return res

        return_value = res.register(method(exec_ctx))
        if res.should_return(): return res
        return res.success(return_value)
        
    def no_visit_method(self, node, context):
        raise Exception(f'No existe execute_{self.name}')

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
        return RTResult().success(Empty())
    execute_print.arg_names = ['value']
        
    def execute_print_ret(self, exec_ctx):
        return RTResult().success(String(str(exec_ctx.symbol_table.get('value'))))
    execute_print_ret.arg_names = ['value']
        
    def execute_input(self, exec_ctx):
        text = input(exec_ctx.symbol_table.get('inputValue?') or "Que me queré decir bro? >")
        return RTResult().success(String(text))
    execute_input.arg_names = ["inputValue?"]

    def execute_input_int(self, exec_ctx):
        while True:
            text = input(exec_ctx.symbol_table.get('inputValue?') or "Tirame un numero: ")
            try:
                number = int(text)
                break
            except ValueError:
                print(f"'{text}' tiene que ser un numero tarao, mandale denuevo")
        return RTResult().success(Number(number))
    execute_input_int.arg_names = ["inputValue?"]

    def execute_clear(self, exec_ctx):
        os.system('cls' if os.name == 'nt' else 'cls') 
        return RTResult().success(Empty())
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
                "Motri me tenes que dar una lista pa poner un elemento",
                exec_ctx
            ))

        list_.elements.append(value)
        return RTResult().success(list_)
    execute_append.arg_names = ["list", "value"]

    def execute_pop(self, exec_ctx):
        list_ = exec_ctx.symbol_table.get("list")
        index = exec_ctx.symbol_table.get("index")

        if not isinstance(list_, List):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Motri me tenes que dar una lista pa rajar un elemento",
                exec_ctx
            ))

        if not isinstance(index, Number):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "CAPO dame el index en el segundo argumento",
                exec_ctx
            ))

        try:
            element = list_.elements.pop(index.value)
        except:
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                detailsMessages["outOfIndex"],
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
                "Tiene que ser una lista el primer argumento crack",
                exec_ctx
            ))

        if not isinstance(listB, List):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "También tiene que ser una lista el segundo crack",
                exec_ctx
            ))

        listA.elements.extend(listB.elements)
        return RTResult().success(listA)
    execute_extend.arg_names = ["listA", "listB"]

    def execute_len(self, exec_ctx):
        value = exec_ctx.symbol_table.get("value")

        if isinstance(value, List):
            return RTResult().success(Number(len(value.elements)))
        if isinstance(value, String):
            return RTResult().success(Number(len(value.value)))

        return RTResult().failure(RTError(
            self.pos_start, self.pos_end,
            "Che el len tiene que tener una lista o un string",
            exec_ctx
            ))

    execute_len.arg_names = ["value"]

    def execute_run(self, exec_ctx):
        fn = exec_ctx.symbol_table.get("fn")

        if not isinstance(fn, String):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Dame un string papá",
                exec_ctx
                ))
        
        if fn.value[-4:] != ".che":
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "CAPO tiene que ser un archivo .che , que te pensas?",
                exec_ctx
                ))

        fn = fn.value

        try:
            with open(fn, "r") as f:
                script = f.read()
        except Exception as e:
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                f"Que pasó perro? No arrancó? Algo va mal en \"{fn}\"\n" + str(e),
                exec_ctx
                ))
        from CheLang.cheLangCompiler import run
        _, error = run(fn, script)
        
        if error:
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                f"Che \"{fn}\" no funcó, fijate que onda.\n" +
                error.as_string(),
                exec_ctx
                ))

        return RTResult().success(Empty())
    execute_run.arg_names = ["fn"]

    def execute_hola(self, exec_ctx):
        print("Que onda perro? Todo piola?")
        return RTResult().success(Empty())
    execute_hola.arg_names = []

    def execute_argentina(self, exec_ctx):
        import ctypes
        import os
        from playsound import playsound
        print("\n¡VIVA LA PATRIA!\n\n¡VIVA!\n")
        notDone = True
        try:
            imageUri = os.path.abspath(os.environ["CheLangPath"]) + "\\assets\\Argentina.jpg"
            soundUri = os.path.abspath(os.environ["CheLangPath"]) + "\\assets\\Malvinas.mp3"
            os.startfile(imageUri)
            notDone = False
            ctypes.windll.user32.SystemParametersInfoW(20, 0, imageUri , 0)
            playsound(soundUri)
        except:
            if notDone:
                try:
                    imageUri = os.path.abspath(os.getcwd()) + "\\assets\\Argentina.jpg"
                    soundUri = os.path.abspath(os.getcwd()) + "\\assets\\Malvinas.mp3"
                    os.startfile(imageUri)
                    ctypes.windll.user32.SystemParametersInfoW(20, 0, imageUri , 0)
                    playsound(soundUri)
                except FileNotFoundError:
                    print("Pasó algo, no pude cargar las cosas... Para mi es culpa del kernel imperialista...")
        finally:
            return RTResult().success(Empty())
    execute_argentina.arg_names = []

    def execute_thief(self, exec_ctx):
        from time import sleep
        print("\nSi entra el chorro no lo podes amasijar en el patio porque despues dicen que se cayo de la medianera.", end="\n\n")
        sleep(4)
        print("Vos lo tenes que llevar al lugar mas recóndito de tu casa.", end="\n\n")
        sleep(2)
        print("Al ultimo dormitorio.", end="\n\n")
        sleep(1.5)
        print("Y si es posible al sótano.", end="\n\n")
        sleep(1.5)
        print("Bien escondido.", end="\n\n")
        sleep(2)
        print("Y ahí lo reventas a balazos. Le tiras todos los tiros.", end="\n\n")
        sleep(3)
        print("No uno, porque vas a ser habil tirador y te comes un garron de la gran flauta.", end="\n\n")
        sleep(3)
        print("Vos estabas en un estado de emocion violenta y de locura.", end="\n\n")
        sleep(2)
        print("Lo rreventaste a tiros, le vaciaste todo el cargador.", end="\n\n")
        sleep(2)
        print("Le zapateas arriba. Lo meas. Para demostrar tu estado de locura y de inconsciencia temporal.", end="\n\n")
        sleep(3.3)
        print("¿Me explico?", end="\n\n")
        sleep(1.5)
        print("Ademas tenes que tener una botella de chiv va a mano, te tomas media botella,", end="\n\n")
        sleep(3)
        print("y si tenes un sobre de cocaina, papoteate y vas al juzgado así. *Movimientos epilepticos*", end="\n\n")
        sleep(3)
        print("Sos inimputable hermano.", end="\n\n")
        sleep(2.3)
        print("En diez dias salis.", end="\n\n")
        sleep(1)
        return RTResult().success(Empty())
    execute_thief.arg_names = []

    def execute_exit(self, exec_ctx):
        import sys
        print('Nos vemos wachin! Aguante Argentina!')
        sys.exit(0)
        return RTResult().success(Empty())
    execute_exit.arg_names = []
    
    
    def execute_sleep(self, exec_ctx):
        from time import sleep
        n = exec_ctx.symbol_table.get("value")
        if isinstance(n, Number):
            sleep(n.value)
        else:
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Flaco dame una cantidad de segundos, no cualquier cosa",
                exec_ctx
            ))
        return RTResult().success(Empty())
    execute_sleep.arg_names = ["value"]

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
BuiltInFunction.len         = BuiltInFunction("len")
BuiltInFunction.run         = BuiltInFunction("run")
BuiltInFunction.hola        = BuiltInFunction("hola")
BuiltInFunction.argentina   = BuiltInFunction("argentina")
BuiltInFunction.thief       = BuiltInFunction("thief")
BuiltInFunction.exit        = BuiltInFunction("exit")
BuiltInFunction.sleep        = BuiltInFunction("sleep")
