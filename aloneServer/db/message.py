class Message:
    def __init__(self):
        self.returnMessage = None
        self.returnBool = None

    def getMessage(self):
        return self.returnMessage

    def getBool(self):
        return self.returnBool

class SuccessMessage(Message):
    def __init__(self):
        self.returnMessage = "success"

class FailMessage(Message):
    def __init__(self):
        self.returnMessage = "fail"

class CompMessage(Message):
    def __init__(self, _obj):
        if str(_obj) == SuccessMessage().getMessage():
           self.returnBool = True
        elif str(_obj) == FailMessage().getMessage():
           self.returnBool = False