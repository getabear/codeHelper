from key_hook import KeyBuf
from language_util import LanguageUtil
from .policy import Policy


class SeqPolicy(Policy):
    def __init__(self, sequence: set[str], language: str, language_util: LanguageUtil):
        super().__init__()
        self.seq = sequence
        self.language = language
        self.language_util = language_util


    def condition(self, buffer: KeyBuf):
        s = buffer.last_str()
        for i in range(len(s)):
            if s[i:] in self.seq:
                return True

        return False

    def action(self):
        self.language_util.change_language(self.language)

