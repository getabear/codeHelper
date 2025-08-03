from collections import deque
from functools import cache
from key_hook.keyboard_hook import KeyBuf


# 用来检测输入的字符串是否是中文的拼音
class WordDetect:
    def __init__(self, words_file):
        self.words = set()
        with open(words_file, "r", encoding='utf-8') as f:
            for line in f:
                # 删除末尾的空格
                word = line[:-1]
                self.words.add(word)

    # 检测字符串是否能够组成有效的拼音
    def match_word(self, s):
        @cache
        def dfs(word, dep):
            if dep == len(s):
                return not word
            word += s[dep]
            ret = False
            if word in self.words:
                ret = dfs('', dep + 1)
            ret = ret or dfs(word, dep + 1)
            return ret
        if len(s) == 0:
            return False
        return dfs('', 0)
    # 魔术方法, 匹配的话返回匹配的字符串， 否则返回None
    def __call__(self, s):
        if self.match_word(s):
            return s
        return None



if __name__ == "__main__":
    a = WordDetect("../Pinyin/pinyin.txt")
    print(a.words)
    print(len(a.words))     # 424
    print(a.match_word("nihao"))
