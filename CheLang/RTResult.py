
###################################################
# RUNTIME RESULT
###################################################
class RTResult:
    def __init__(self):
        self.value = None
        self.error = None

    ###############################
    # REGISTER METHOD 
    ###############################
    def register(self, res):
        if res.error: self.error = res.error
        return res.value

    ###############################
    # SUCCESS METHOD   - ganadorr -
    ###############################
    def success(self, value):
        self.value = value
        return self
    ###############################
    # FAILURE METHOD   - fracasau -
    ###############################
    def failure(self, error):
        self. error = error
        return self

