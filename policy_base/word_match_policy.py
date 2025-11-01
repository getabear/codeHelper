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
    def __init__(self, language_util: LanguageUtil):
        super().__init__()
        self.word_detect = WordDetect("Pinyin/pinyin.txt")
        # match 匹配成功后变为 matched. matched 等待按键，按键匹配，状态切换到 act， 按键不匹配状态切换回match
        self.word = ""
        self.util = language_util
        # 控制键盘输入
        self.kc = Controller()


    def condition(self, buffer: deque):
        # print("WordPolicy 当前的buf为: ", buffer)

        _str = self.get_curstr(buffer)
        # 保证处理的是全英文
        cur_str = "".join(_str)
        print("WordPolicy: 当前的cur_str = ", cur_str)
        # 智能检测拼音，应对中文和英文同时存在的情况
        for i in range(len(cur_str)):
            if self.word_detect.match_word(cur_str[i:]):
                self.word = cur_str[i:]  # 记录当前的拼英
                return True
        return False


    def action(self):
        self.util.change_language("Chinese")
        print("模拟输入的字符串是: {}".format(self.word))
        for i in range(len(self.word)):
            self.kc.press(Key.backspace)
            self.kc.release(Key.backspace)
        self.kc.type(self.word)







