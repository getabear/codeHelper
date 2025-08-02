class Policy:
    def __init__(self):
        pass

    def condition(self, buffer):
        pass

    def action(self):
        pass

    def __call__(self, buffer):
        if self.condition(buffer):
            self.action()
