import ctypes
import os
import threading

from PIL import Image

import pystray

from key_hook import ClipHelper
from language_util import LanguageUtil

from policy_base.symbol_policy import SymbolPolicy
from policy_base.word_match_policy import WordPolicy



# 获取控制台窗口句柄
def get_console_window():
    kernel32 = ctypes.windll.kernel32
    return kernel32.GetConsoleWindow()

# 显示或隐藏控制台窗口
def toggle_console(show=None):
    console_window = get_console_window()
    if console_window:
        user32 = ctypes.windll.user32
        if show is None:
            # 自动切换状态
            if user32.IsWindowVisible(console_window):
                show = False
            else:
                show = True
        if show:
            user32.ShowWindow(console_window, 1)  # SW_SHOWNORMAL
        else:
            user32.ShowWindow(console_window, 0)  # SW_HIDE


def on_quit(icon):
    icon.stop()
    os._exit(0)

def load_icon():
    try:
        image = Image.open("helper.png")
        return image
    except FileNotFoundError:
        print("文件未找到！")
def show_window():
    toggle_console(True)


def hide_window():
    toggle_console(False)


def setup_tray():
    icon = pystray.Icon(
        "codeHelper",
        icon=load_icon(),
        title="输入法切换工具",
        menu=pystray.Menu(
            pystray.MenuItem("显示", show_window),
            pystray.MenuItem("隐藏", hide_window),
            pystray.MenuItem("退出", on_quit),
        )
    )
    return icon

def _main():


    helper = ClipHelper()
    util = LanguageUtil()
    policy = WordPolicy(util)
    # relus = {"//":"Chinese", "#": "Chinese"}
    # policy2 = SeqPolicy(relus, util)
    policy3 = SymbolPolicy(util)
    helper.add_callback(policy)
    helper.add_callback(policy3)
    helper.start_hook()



if __name__ == '__main__':
    threading.Thread(target=_main, daemon=True).start()
    tray_icon = setup_tray()
    tray_icon.run()
