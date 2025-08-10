import copy
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

    def pop(self):
        return self.buf.pop()

    # 返回以特殊字符分割开的最后一个字符串
    @staticmethod
    def current_str(buf):
        if not buf:
            return ""
        idx, buf = 0, list(buf)
        for i in range(len(buf) - 1, -1, -1):
            idx = i
            if isinstance(buf[i], Key):
                break
        if idx == 0 and not isinstance(buf[idx], Key):
            idx = -1
        return ''.join(buf[idx + 1:])

    def get_buf(self):
        return copy.copy(self.buf)

    def set_buf(self, buf: deque):
        self.buf.clear()
        self.buf = buf

# callback是回调函数，接收按键的buffer作为参数
class KeyHook:
    def __init__(self):
        self.key_buffer = KeyBuf(20)
        self.change = False
        self.callbacks = []
        self.listener = None
        self.virtual = False
        self.kc = Controller()

    def start_hook(self):
        def on_release(key):
            self.change = True
            try:
                print('字母键： {} 被释放'.format(key.char))
                self.key_buffer.append(key.char)
            except AttributeError:
                print('特殊键： {} 被释放'.format(key))
                if key == Key.backspace:
                    if self.key_buffer.buf:
                        self.key_buffer.pop()
                else:
                    # self.key_buffer.buf.clear()
                    self.key_buffer.append(key)
            print("hook buf: ", self.key_buffer.buf)
            if self.callbacks:
                for callback in self.callbacks:
                    if callback(self.key_buffer.get_buf()):     # 每次只能有一个策略生效
                        self.key_buffer.buf.clear()
                        break

        self.listener = keyboard.Listener(
                on_release=on_release)
        self.listener.start()

    def stop_hook(self):
        self.listener.stop()

    def add_callback(self, callback):
        self.callbacks.append(callback)



if __name__ == "__main__":
    tmp = KeyHook()
    tmp.start_hook()
    while True:
        sleep(2)
        print(tmp.key_buffer.buf)
