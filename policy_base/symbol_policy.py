from collections import deque
from time import sleep

from pynput.keyboard import Controller, Key

from language_util import LanguageUtil
from policy_base import Policy


class SymbolPolicy(Policy):
    def __init__(self, language_util: LanguageUtil, ensure_key=("`", "`")):
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
            "\\": "、",
            "——": "_"
        }
        self.ch_map = dict()
        for k, v in self.eng_map.items():
            self.ch_map[v] = k
        self.word = None
        self.old_lang = None

    def recovery(self):
        if self.old_lang:
            self.util.change_language(self.old_lang)
        self.old_lang = None

    def condition(self, buffer: deque):
        self.word = None
        ensure_key = buffer.pop() if buffer else None
        language = self.util.detect_language()
        print("SymbolPolicy buf: ", buffer)
        last_key = None
        while buffer:
            item = buffer.pop()
            if not isinstance(item, Key):
                last_key = item
                break
        print("SymbolPolicy last_key: ", last_key)
        if language == "Chinese" and ensure_key and ensure_key == self.ensure_key[0]:
            self.util.change_language("English")
            self.word = last_key
            self.old_lang = "Chinese"
        elif ensure_key and ensure_key == self.ensure_key[1]:
            self.word = self.eng_map.get(last_key, None)

        return self.word is not None


    def action(self):
        for i in range(2):
            self.kc.press(Key.backspace)
            self.kc.release(Key.backspace)
        print("SymbolPolicy self.word: ", self.word)
        self.kc.type(self.word)
        self.recovery()


if __name__ == "__main__":
    kc = Controller()
    sleep(1)
    kc.type("。")

# .。