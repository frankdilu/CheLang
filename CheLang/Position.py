
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
