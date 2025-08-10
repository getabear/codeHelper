from collections import deque
from time import sleep

from key_hook import KeyBuf, KeyHook
from .policy import Policy
from .word_detect import WordDetect
from language_util import LanguageUtil
from pynput.keyboard import Controller, Key
import sys
import os


# 拼英匹配成功直接切换中文
class WordPolicy(Policy):
    def __init__(self, language_util: LanguageUtil, ensure_key="`"):
        super().__init__()
        self.word_detect = WordDetect("Pinyin/pinyin.txt")
        # 匹配成功后，需要用户按下特定按键才执行操作
        self.ensure_key = ensure_key
        # match 匹配成功后变为 matched. matched 等待按键，按键匹配，状态切换到 act， 按键不匹配状态切换回match
        self.word = ""
        self.util = language_util
        # 控制键盘输入
        self.kc = Controller()


    def condition(self, buffer: deque):
        print("当前的buf为：", buffer)
        end_key = buffer.pop() if buffer else None
        flag = False
        try:
            if end_key.char == self.ensure_key:
                flag = True
        except AttributeError:
            if end_key == self.ensure_key:
                flag = True

        if flag:
            print("当前的flag = ", flag)
            cur_str = KeyBuf.current_str(buffer)
            if self.word_detect.match_word(cur_str):
                self.word = cur_str  # 记录当前的拼英
                return True
        return False


    def action(self):
        self.util.change_language("Chinese")
        print("模拟输入的字符串是: {}。".format(self.word))
        for i in range(len(self.word) + 1):
            self.kc.press(Key.backspace)
            self.kc.release(Key.backspace)
        self.kc.type(self.word)







