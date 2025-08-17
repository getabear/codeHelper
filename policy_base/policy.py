from collections import deque


class Policy:
    def __init__(self):
        pass

    def condition(self, buffer: deque):
        pass

    def action(self):
        pass

    def __call__(self, buffer: deque):
        if self.condition(buffer):
            self.action()
            return True
        return False
