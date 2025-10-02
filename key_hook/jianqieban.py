import time
from collections import deque

import pyperclip
from pynput import keyboard
from pynput.keyboard import Controller, Key


def get_text_to_line_start():

    old_text = pyperclip.paste()

    # 创建键盘控制器
    key_board = Controller()

    # 模拟按下 Shift + Home 键
    key_board.press(Key.shift)
    key_board.press(Key.home)
    key_board.release(Key.home)
    key_board.release(Key.shift)

    # 等待选择完成
    time.sleep(0.1)

    # 复制选中的文本
    key_board.press(Key.ctrl_l)  # 对于 Windows 使用 Key.ctrl
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
        # 获取文本的快捷键
        self.hotkeys = {
            frozenset([Key.f2]): "F2",
        }

        self.press_keys = set()
        self.is_get_text = False

    def add_callback(self, callback):
        self.callbacks.append(callback)


    def start_hook(self):
        def on_press(key):
            # print(key)
            try:
                self.press_keys.add(key)
                # print(key)
            except AttributeError:
                print("ERROR: class Clip() on_click error!")

            for key, value in self.hotkeys.items():
                # 检测到快捷键触发事件
                if key.issubset(self.press_keys) and not self.is_get_text:
                    self.is_get_text = True

        def on_release(key):
            # discard相比remove，当key不存在的时候，不会抛出异常
            self.press_keys.discard(key)
            if self.is_get_text:
                text = get_text_to_line_start()
                for callback in self.callbacks:
                    if callback(deque(list(text))):
                        break
                self.is_get_text = False

        # 开启线程，监听键盘输入事件
        self.listener = keyboard.Listener(on_press=on_press, on_release=on_release)
        self.listener.start()


