from time import sleep

from pynput import keyboard
from pynput.keyboard import Controller
from collections import deque
from pynput.keyboard import Key


class KeyBuf:
    def __init__(self, max_len: int = 20):
        self.buf = deque(maxlen=max_len)

    def append(self, item):
        self.buf.append(item)

    def popleft(self):
        return self.buf.popleft()

    def pop(self):
        return self.buf.pop()

    # 返回以特殊字符分割开的最后一个字符串
    def last_str(self):
        if not self.buf:
            return ""
        idx, buf = 0, list(self.buf)
        for i in range(len(buf) - 1, -1, -1):
            idx = i
            if isinstance(buf[i], Key):
                break
        if idx == 0 and not isinstance(buf[idx], Key):
            idx = -1
        return ''.join(buf[idx + 1:])

    def __getitem__(self, item):
        return self.buf[item]

    def clear(self):
        self.buf.clear()


# callback是回调函数，接收按键的buffer作为参数
class KeyHook:
    def __init__(self):
        self.key_buffer = KeyBuf(20)
        self.change = False
        self.callback = None
        self.listener = None
        self.virtual = False
        self.kc = Controller()

    def start_hook(self):
        def on_release(key):
            self.change = True
            try:
                print('字母键： {} 被释放'.format(key.char))
                if self.callback and key.char == '`':
                    self.callback(self.key_buffer)
                else:
                    self.key_buffer.append(key.char)
            except AttributeError:
                print('特殊键： {} 被释放'.format(key))
                if key == Key.backspace:
                    if self.key_buffer.buf:
                        self.key_buffer.pop()
                else:
                    self.key_buffer.append(key)

        self.listener = keyboard.Listener(
                on_release=on_release)
        self.listener.start()

    def stop_hook(self):
        self.listener.stop()

    def key_input(self, text):
        self.kc.type(text)  # 模拟输入

    def get_buffer(self):
        # 要是有按键更新才返回buffer
        if self.change:
            self.change = False
            return self.key_buffer
        return None

    def set_callback(self, callback):
        self.callback = callback



if __name__ == "__main__":
    tmp = KeyHook()
    tmp.start_hook()
    while True:
        sleep(2)
        # print(tmp.get_buffer())
        tmp.key_input("nihao")
        print(tmp.key_buffer.buf)
