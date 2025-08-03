from pynput.keyboard import Key

from shift_policy import ShiftPolicies
from key_hook import KeyHook
from language_util import LanguageUtil

if __name__ == '__main__':
    hook = KeyHook()
    util = LanguageUtil()
    policies = ShiftPolicies(util, hook)
    hook.set_callback(policies)
    hook.start_hook()
    while True:
        pass

# hello 你好