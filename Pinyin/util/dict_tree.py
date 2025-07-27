# 字典树的数据结构
class DictTreeNode:
    def __init__(self):
        self.has_end = False
        self.mem = dict()


class DictTree:
    def __init__(self):
        self.root = DictTreeNode()

    def find(self, word):
        head = self.root
        for ch in word:
            if ch not in head.mem:
                return False
            head = head.mem[ch]
        return head.has_end

    def insert(self, word):
        head = self.root
        for ch in word:
            if ch not in head.mem:
                head.mem[ch] = DictTreeNode()
            head = head.mem[ch]

        head.has_end = head.has_end or True
        return True




