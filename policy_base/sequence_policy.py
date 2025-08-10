from collections import deque

from key_hook import KeyBuf
from language_util import LanguageUtil
from .policy import Policy


class SeqPolicy(Policy):
    def __init__(self, rules: dict, language_util: LanguageUtil):
        super().__init__()
        self.rules = rules
        self.language_util = language_util
        self.language = None

    def condition(self, buffer: deque):
        buf = list(buffer)
        for seq in self.rules.keys():
            try:
                if "".join(buf[-len(seq):]) == seq:
                    self.language = self.rules[seq]
                    return True
            except TypeError:
                continue
        return False

    def action(self):
        if self.language:
            self.language_util.change_language(self.language)

