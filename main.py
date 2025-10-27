import ctypes
import os
import threading
import time
import signal
import sys

from key_hook import ClipHelper
from language_util import LanguageUtil
from policy_base.symbol_policy import SymbolPolicy
from policy_base.word_match_policy import WordPolicy

# 全局标志，用于控制程序退出
running = True


def signal_handler(sig, frame):
    """处理Ctrl+C信号"""
    global running
    print("\n正在退出程序...")
    running = False
    # 给线程一些时间来清理
    time.sleep(0.5)
    sys.exit(0)


def _main():
    """主要的键盘钩子逻辑"""
    try:
        print("启动键盘钩子服务...")
        helper = ClipHelper()
        util = LanguageUtil()
        policy = WordPolicy(util)
        policy3 = SymbolPolicy(util)

        helper.add_callback(policy)
        helper.add_callback(policy3)
        print("程序正在运行中...")
        helper.start_hook()

    except Exception as e:
        print(f"键盘钩子线程异常: {e}")


def main():
    """主函数"""
    # 注册信号处理
    signal.signal(signal.SIGINT, signal_handler)

    print("=" * 50)
    print("输入法切换工具")
    print("=" * 50)

    # 在后台线程中运行键盘钩子
    hook_thread = threading.Thread(target=_main, daemon=True)
    hook_thread.start()

    # 主线程保持运行，等待退出信号
    try:
        while running:
            time.sleep(0.2)
    except KeyboardInterrupt:
        signal_handler(None, None)


if __name__ == '__main__':
    main()

#