import traceback

from pynput.keyboard import Key

from key_hook import KeyHook
from language_util import LanguageUtil
from policy_base.sequence_policy import SeqPolicy
from policy_base.word_match_policy import WordPolicy
from pynput.keyboard import Key

if __name__ == '__main__':
    try:
        hook = KeyHook()
        util = LanguageUtil()
        policy = WordPolicy(util)
        relus = {"//":"Chinese", "#": "Chinese"}
        policy2 = SeqPolicy(relus, util)
        hook.add_callback(policy)
        hook.start_hook()

        hook.listener.join()

    except Exception as e:
        with open("error.log", "w") as f:
            f.write(traceback.format_exc())
        print("程序出错，请查看 error.log")
        input("按 Enter 键退出...")
#