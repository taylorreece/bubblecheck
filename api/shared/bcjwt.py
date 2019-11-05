class BCJWT(object):
    def __init__(self):
        self.secret = ''
    def set_secret(self, secret):
        self.secret = secret
    def get_secret(self):
        return self.secret

bcjwt_secret = BCJWT()