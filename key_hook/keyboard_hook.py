import copy
from time import sleep

from pynput import keyboard
from pynput.keyboard import Controller
from collections import deque
from pynput.keyboard import Key


class KeyBuf:
    def __init__(self, max_len: int = 50):
        self.buf = deque(maxlen=max_len)

    def append(self, item):
        self.buf.append(item)

    def pop(self):
        return self.buf.pop()

    def get_buf(self):
        return copy.copy(self.buf)

    def set_buf(self, buf: deque):
        self.buf.clear()
        self.buf = buf

# callback是回调函数，接收按键的buffer作为参数
class KeyHook:
    def __init__(self):
        self.key_buffer = KeyBuf(50)
        self.change = False
        self.callbacks = []
        self.listener = None
        self.virtual = False
        self.kc = Controller()

    def start_hook(self):
        def on_release(key):
            self.change = True
            try:
                print('Keyhook 字母键： {} 被释放'.format(key.char))
                self.key_buffer.append(key.char)
            except AttributeError:
                print('Keyhook 特殊键： {} 被释放'.format(key))
                if key == Key.backspace:
                    # 删除可见字符
                    while self.key_buffer.buf:
                        item = self.key_buffer.pop()
                        if isinstance(item, str):
                            break
                        elif isinstance(item, Key):
                            if item == Key.space or item == Key.tab:
                                break

                # elif key == Key.enter:
                #     self.key_buffer.buf.clear()
                else:
                    self.key_buffer.append(key)

            print("Keyhook buf: ", self.key_buffer.buf)
            if self.callbacks:
                for callback in self.callbacks:
                    if callback(self.key_buffer.get_buf()):     # 每次只能有一个策略生效
                        self.key_buffer.buf.clear()
                        break

        with keyboard.Events() as events:
            for event in events:
                if isinstance(event, keyboard.Events.Release):
                    on_release(event.key)


    def stop_hook(self):
        # self.listener.stop()
        pass

    def add_callback(self, callback):
        self.callbacks.append(callback)



if __name__ == "__main__":
    tmp = KeyHook()
    tmp.start_hook()
    while True:
        sleep(2)
        print(tmp.key_buffer.buf)

