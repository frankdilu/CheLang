
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


