from collections import deque

from pynput.keyboard import Controller, Key

from language_util import LanguageUtil
from policy_base import Policy


class SymbolPolicy(Policy):
    def __init__(self, language_util: LanguageUtil, ensure_key=("·", "`")):
        super().__init__()
        self.util = language_util
        self.ensure_key = ensure_key
        self.kc = Controller()
        self.eng_map = {
            "-": "-",
            ".": "。",
            "<": "《",
            ">": "》",
            ",": "，",
            ":": "：",
            "\\": "、"
        }
        self.ch_map = dict()
        for k, v in self.eng_map.items():
            self.ch_map[v] = k
        self.word = None

    def condition(self, buffer: deque):
        self.word = None
        ensure_key = buffer.pop() if buffer else None
        language = self.util.detect_language()
        last_key = buffer.pop() if buffer else None
        if language == "Chinese" and ensure_key and ensure_key == self.ensure_key[0]:
            self.word = self.ch_map.get(last_key, None)
        elif ensure_key and ensure_key == self.ensure_key[1]:
            self.word = self.eng_map.get(last_key, None)

        return self.word is not None


    def action(self):
        for i in range(2):
            self.kc.press(Key.backspace)
            self.kc.release(Key.backspace)
        self.kc.type(self.word)
