from time import sleep

from pynput import keyboard
from pynput.keyboard import Controller
from collections import deque

class KeyBuf:
    def __init__(self, max_len: int=20):
        self.buf = deque(maxlen=max_len)

    def append(self, item):
        self.buf.append(item)

    def popleft(self):
        return self.buf.popleft()
    # 返回以特殊字符分割开的最后一个字符串
    def last_str(self):
        idx, buf = 0, list(self.buf)
        for i in range(len(buf) - 1, -1, 0):
            idx += 1
            if buf[i] == ' ' or len(buf[i]) != 1:
                break
        return ''.join(buf[idx + 1: ])

# callback是回调函数，接收按键的buffer作为参数
class KeyHook:
    def __init__(self):
        self.key_buffer = KeyBuf(20)
        # 用于判定是否是模拟用户输入
        self.virtual_input = False
        self.change = False

        def on_press(key):
            if not self.virtual_input:
                self.change = True
                try:
                    print('字母键： {} 被按下'.format(key.char))
                    self.key_buffer.append(key.char)
                except AttributeError:
                    print('特殊键： {} 被按下'.format(key))
                    self.key_buffer.append(key.name)

        self.listener = keyboard.Listener(
            on_press=on_press)
        self.kc = Controller()

    def start_hook(self):
        # 监听启动方式2：非阻断式
        self.listener.start()

    def stop_hook(self):
        self.listener.stop()

    def key_input(self, text):
        self.virtual_input = True
        self.kc.type(text)
        self.virtual_input = False

    def get_buffer(self):
        # 要是有按键更新才返回buffer
        if self.change:
            self.change = False
            return self.key_buffer
        return None
# 123
if __name__ == "__main__":
    tmp = KeyHook()
    tmp.start_hook()
    while True:
        sleep(2)
        # print(tmp.get_buffer())
        # tmp.key_input("nihao")