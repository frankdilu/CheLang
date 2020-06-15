
###################################################
# PARSE RESULT   - ete se fija si hiciste macanas -
###################################################
class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None
        self.advance_count = 0
        self.to_reverse_count = 0

    ###############################
    # REGISTER ADVANCEMENT  -count-
    ###############################
    def register_advancement(self):
        self.last_registered_advance_count = 1
        self.advance_count += 1

    ###############################
    # REGISTER METHOD - toma nota -
    ###############################
    def register(self, res):
        self.last_registered_advance_count = res.advance_count
        self.advance_count += res.advance_count
        if res.error: self.error = res.error
        return res.node

    def try_register(self, res):
        if res.error:
            self.to_reverse_count = res.advance_count
            return None
        return self.register(res)

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
        if not self.error or self.last_registered_advance_count  == 0:
            self.error = error
        return self
