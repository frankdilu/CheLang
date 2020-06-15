
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
