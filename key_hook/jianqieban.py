import time
from collections import deque

import pyperclip
import pynput
from pefile import set_format
from pynput.keyboard import Controller, Key
import keyboard

def get_text_to_line_start(keys=None):

    old_text = pyperclip.paste()

    # 创建键盘控制器
    key_board = Controller()

    # 释放转换的快捷键
    for key in keys:
        key_board.release(key)

    # 模拟按下 Shift + Home 键
    key_board.press(Key.shift)
    key_board.press(Key.home)
    key_board.release(Key.home)
    key_board.release(Key.shift)

    # 等待选择完成
    time.sleep(0.1)

    # 复制选中的文本
    key_board.press(Key.ctrl_l)  # 对于 Windows 使用 Key.ctrl
    time.sleep(0.1)
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

class ClipHelper:
    def __init__(self):
        self.callbacks = []
        self.listener = None
        # print(self.hotkeys)

        self.press_keys = set()
        self.is_get_text = False

        def change_stat1():
            self.is_get_text = True
            self.press_keys.add(Key.f2)
            print("self.is_get_text = True")

        def change_stat2():
            self.is_get_text = True
            self.press_keys.add('`')
            self.press_keys.add(Key.alt_l)
            print("self.is_get_text = True")

        keyboard.add_hotkey('f2', change_stat1)
        keyboard.add_hotkey('alt+`', change_stat2)


    def add_callback(self, callback):
        self.callbacks.append(callback)


    def start_hook(self):
        def on_release(key):
            if self.is_get_text:
                text = get_text_to_line_start(self.press_keys)
                self.press_keys.clear()
                for callback in self.callbacks:
                    if callback(deque(list(text))):
                        break
                self.is_get_text = False

        # 开启线程，监听键盘输入事件
        self.listener = pynput.keyboard.Listener(on_release=on_release)
        self.listener.start()


 # nihao