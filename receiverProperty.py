class ReceiverProperty:
    def __init__(self, code, receiver_value):
        self.code = code
        self.receiver_value = receiver_value

    def get_code(self):
        return self.code

    def get_value(self):
        return self.receiver_value
