from time import sleep

from pynput import keyboard
from pynput.keyboard import Controller
from collections import deque


# callback是回调函数，接收按键的buffer作为参数
class KeyHook:
    def __init__(self, callback=None):
        self.key_buffer = deque(maxlen=20)
        self.callbacks = []
        if callback is not None:
            self.callbacks.append(callback)
        # 用于判定是否是模拟用户输入
        self.virtual_input = False

        def on_press(key):
            if not self.virtual_input:
                try:
                    print('字母键： {} 被按下'.format(key.char))
                    self.key_buffer.append(key.char)
                except AttributeError:
                    print('特殊键： {} 被按下'.format(key))
                    self.key_buffer.append(key)

                # 找到最后的不带分格的字符串
                idx = 0
                for i in range(len(self.key_buffer) - 1, -1, -1):
                    idx = i
                    if (not isinstance(self.key_buffer[i], str) or
                            not (self.key_buffer[i].isalpha() or self.key_buffer[i].isdigit())):
                        break
                s = ''.join(list(self.key_buffer)[idx + 1:])

                # 当按键按下的时候（观察者模式）
                for cbk in self.callbacks:
                    cbk(s)

        self.listener = keyboard.Listener(
            on_press=on_press)
        self.kc = Controller()

    def add_callback(self, callback):
        self.callbacks.append(callback)

    def start_hook(self):
        # 监听启动方式2：非阻断式
        self.listener.start()

    def stop_hook(self):
        self.listener.stop()

    def get_buffer(self):
        return self.key_buffer

    def key_input(self, text):
        self.virtual_input = True
        self.kc.type(text)
        self.virtual_input = False


if __name__ == "__main__":
    tmp = KeyHook()
    tmp.start_hook()
    while True:
        sleep(2)
        tmp.key_input("nihao")