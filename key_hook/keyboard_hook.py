import copy
import threading
from time import sleep, time

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
        self.callbacks = []
        self.listener = None
        self.virtual = False
        self.kc = Controller()
        # 控制输入是否是模拟，模拟输入不进行监听
        self.is_simulate = False
        self.event = threading.Event()
        self.mutex = threading.Lock()
        self.clear_code = [Key.insert, Key.insert, Key.insert, Key.insert, Key.insert, Key.insert]
        self.last_time = time()

    def clear_buf(self):
        for key in self.clear_code:
            self.kc.press(key)
            self.kc.release(key)
        print("清除输入！")

    def start_hook(self):
        def on_press(key):
            # 超过时间，自动清除buf缓冲区
            now = time()
            if now - self.last_time > 10:
                self.key_buffer.buf.clear()
            self.last_time = now
            try:
                # print('Keyhook 字母键： {} 被释放'.format(key.char))
                self.key_buffer.append(key.char)
            except AttributeError:
                # print('Keyhook 特殊键： {} 被释放'.format(key))
                if key == Key.backspace:
                    # 删除可见字符
                    while self.key_buffer.buf:
                        item = self.key_buffer.pop()
                        if isinstance(item, str):
                            break
                        elif isinstance(item, Key):
                            if item == Key.space or item == Key.tab:
                                break
                else:
                    self.key_buffer.append(key)

            # 模拟输入不应该添加进来
            if len(self.key_buffer.buf) >= len(self.clear_code):
                last_code = list(self.key_buffer.buf)[-(len(self.clear_code)):]
                if last_code == self.clear_code:
                    # print("last code: {}, key hook clear!".format(last_code))
                    print("key hook clear!")
                    self.key_buffer.buf.clear()
                    return

        def on_release(key):
            self.event.set()

        # 开启线程，监听键盘输入事件
        self.listener = keyboard.Listener(on_press=on_press, on_release=on_release)
        self.listener.start()

    def stop_hook(self):
        self.listener.stop()
        pass

    def add_callback(self, callback):
        self.callbacks.append(callback)

    def notify_callbacks(self):
        while True:
            self.event.wait()
            self.event.clear()
            print("key hook: ", self.key_buffer.buf)
            for callback in self.callbacks:
                if callback(self.key_buffer.get_buf()):
                    # 由于按键事件触发可能总是滞后，导致无法区分模拟还是人工输入
                    # 输入特定clear按键，触发清除数据的流程（因为下面的执行在模拟输入后再次输入，是最后执行的）
                    self.clear_buf()
                    break



if __name__ == "__main__":
    tmp = KeyHook()
    tmp.start_hook()
    while True:
        sleep(2)
        print(tmp.key_buffer.buf)
