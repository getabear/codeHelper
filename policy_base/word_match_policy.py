from time import sleep

from key_hook import KeyBuf, KeyHook
from .policy import Policy
from .word_detect import WordDetect
from language_util import LanguageUtil
from pynput.keyboard import Key


# 拼英匹配成功直接切换中文
class WordPolicy(Policy):
    def __init__(self, ensure_key, key_hook: KeyHook, language_util: LanguageUtil):
        super().__init__()
        self.word_detect = WordDetect("Pinyin/pinyin.txt")
        # 匹配成功后，需要用户按下特定按键才执行操作
        self.ensure_key = ensure_key
        # match 匹配成功后变为 matched. matched 等待按键，按键匹配，状态切换到 act， 按键不匹配状态切换回match
        self.word = ""
        self.util = language_util
        self.key_hook = key_hook


    def condition(self, buffer: KeyBuf):
        print("当前的拼英为: {}.".format(buffer.last_str()))
        if self.word_detect.match_word(buffer.last_str()):
            self.word = buffer.last_str()  # 记录当前的拼英
            return True
        return False

    def action(self):
        self.util.change_language("Chinese")
        print("模拟输入的字符串是: {}。".format(self.word))
        # 因为成功的话，切换的快捷键是 `键，输入区会有一个多的
        for i in range(len(self.word) + 1):
            self.key_hook.kc.press(Key.backspace)

        self.key_hook.key_input(self.word)
        # 转换状态
        self.word = ""
        self.key_hook.key_buffer.clear()





