from .stringsWithArrows import *
from .Const import errorMessages, detailsMessages
###################################################
# ERROR SCHEME
###################################################
class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    ###############################
    # AS STRING METHOD - eto sale -
    ###############################
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
        notLooped = True
        while ctx:
            if notLooped:
                result = "Traceback (las ultimas cuestiones que se llamaron):\n" + f" Archivo {pos.fn}, linea {str(pos.ln + 1)}, en {ctx.display_name} (o por ahí, que se yo)\n" + result
                notLooped = False
            else:
                result = f" Archivo {pos.fn}, linea {str(pos.ln + 1)}, en {ctx.display_name} (o por ahí, que se yo)\n" + result
            pos = ctx.parent_entry_pos
            ctx = ctx.parent

        return result

###############################
# LANGUAGE ERROR
###############################
class LanguageThingError(Error):
    def __init__(self, pos_start, pos_end, details=""):
        super().__init__(pos_start, pos_end, errorMessages["languageThings"], details)