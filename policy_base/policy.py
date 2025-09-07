from collections import deque

from pynput.keyboard import Key


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

    def get_curstr(self, buffer: deque):
        ret = []
        n = 0
        while buffer:
            item = buffer.pop()
            if isinstance(item, str):
                # 只添加英文字母
                if item.isalpha():
                    ret.append(item)
                else:
                    break
            elif isinstance(item, Key):
                # 空格，回车，tab都会将其单词隔断
                if item == Key.space or item == Key.tab or item == Key.enter:
                    break
        return ret[::-1]



