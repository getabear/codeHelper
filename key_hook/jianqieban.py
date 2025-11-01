import time
from collections import deque

import pyperclip
import pynput
from pynput import keyboard
from pynput.keyboard import Controller, Key

def get_text_to_line_start(keys=None):

    old_text = pyperclip.paste()

    # 创建键盘控制器
    key_board = Controller()

    # 释放转换的快捷键
    # for key in keys:
    #     key_board.release(key)

    # 模拟按下 Shift + Home 键
    key_board.press(Key.shift)
    key_board.press(Key.home)
    key_board.release(Key.home)
    key_board.release(Key.shift)

    # 等待选择完成
    time.sleep(0.1)

    # 复制选中的文本
    key_board.press(Key.ctrl_l)  # 对于 Windows 使用 Key.ctrl
    # time.sleep(0.1)
    key_board.press('c')
    key_board.release('c')
    key_board.release(Key.ctrl_l)

    # 等待粘贴操作完成
    time.sleep(0.1)

    # 消除选中
    key_board.press(Key.right)
    key_board.release(Key.right)

    # 从剪贴板获取文本
    text_to_line_start = pyperclip.paste()

    # 恢复剪切板数据
    pyperclip.copy(old_text)

    return text_to_line_start



class HotkeyManager:
    def __init__(self):
        self.hotkeys = []
        self.listener = None

    def add_hotkey(self, combination, callback):
        """添加一个快捷键"""
        hotkey = keyboard.HotKey(
            keyboard.HotKey.parse(combination),
            callback)
        self.hotkeys.append(hotkey)

    def start(self):
        """开始监听快捷键"""

        def on_press(key):
            for hotkey in self.hotkeys:
                hotkey.press(self.listener.canonical(key))

        def on_release(key):
            for hotkey in self.hotkeys:
                hotkey.release(self.listener.canonical(key))

        with keyboard.Listener(on_press=on_press, on_release=on_release) as self.listener:
            self.listener.join()




class ClipHelper:
    def __init__(self):
        self.callbacks = []
        self.listener = None
        self.hot_keys = HotkeyManager()


    def add_callback(self, callback):
        self.callbacks.append(callback)


    def start_hook(self):
        def action():
            text = get_text_to_line_start()
            print(f"ClipHelper:{text}")
            for callback in self.callbacks:
                if callback(deque(list(text))):
                    break
        self.hot_keys.add_hotkey("<f2>", action)
        self.hot_keys.add_hotkey("<ctrl>+`", action)

        self.hot_keys.start()




 # nihao