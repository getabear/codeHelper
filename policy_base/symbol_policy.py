from collections import deque
from encodings import search_function
from time import sleep

from pynput.keyboard import Controller, Key

from language_util import LanguageUtil
from policy_base import Policy


class SymbolPolicy(Policy):
    def __init__(self, language_util: LanguageUtil):
        super().__init__()
        self.util = language_util
        self.kc = Controller()
        # 英文符号转换中文map
        self.eng_map = {
            ".": "。",
            "<": "《",
            ">": "》",
            ",": "，",
            ":": "：",
            "\\": "、",
            "_": "——",
            "!": "！",
            ";": "；",
            "\"": "“",
            "\'": "‘",
            "(": "（",
            ")": "）",
            "?": "？",
            "[": "【",
            "]": "】",
            "$": "￥",
            "^": "……",
            "`": "·"
        }
        self.ch_map = {}
        self.symbols = set()
        for key, value in self.eng_map.items():
            self.ch_map[value] = key
            self.symbols.add(key)
            self.symbols.add(value)

        self.word = None



    def condition(self, buffer: deque):
        self.word = None
        # print("SymbolPolicy buf: ", buffer)
        buffer = list(buffer)
        for symbol in self.symbols:
            if symbol == "".join(buffer[-len(symbol):]):
                self.word = symbol
                break

        return self.word is not None


    def action(self):
        print("SymbolPolicy self.word: ", self.word)
        for i in range(len(self.word)):
            self.kc.press(Key.backspace)
            self.kc.release(Key.backspace)

        if self.word in self.eng_map:
            self.kc.type(self.eng_map[self.word])
        else:
            self.kc.type(self.ch_map[self.word])



if __name__ == "__main__":
    kc = Controller()
    sleep(1)
    kc.type("。")

#