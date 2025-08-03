# 输入法切换的策略（可能包含各种各样的策略）
from key_hook import KeyHook, KeyBuf
from language_util import LanguageUtil
from policy_base.sequence_policy import SeqPolicy
from policy_base.word_match_policy import WordPolicy
from pynput.keyboard import Key


class ShiftPolicies:
    def __init__(self, language_util: LanguageUtil, key_hook: KeyHook):
        self.word_policy = WordPolicy(Key.alt_l, key_hook, language_util)
        seq = {"//", "#"}
        self.seq_policy = SeqPolicy(seq, "Chinese", language_util)
        self.policy = [self.word_policy, self.seq_policy]


    def __call__(self, key_buffer: KeyBuf):
        # 为防止策略冲突，只要有一个策略满足后就返回
        for fun in self.policy:
            if fun(key_buffer):
                break





