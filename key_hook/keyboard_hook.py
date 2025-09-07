import copy
import threading
from time import sleep, time

from pynput import keyboard, mouse
from pynput.keyboard import Controller
from collections import deque
from pynput.keyboard import Key

from language_util import LanguageUtil


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
        self.mouse_listener = None


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
                # 中文输入下，不记录数字，防止输入滞后按下数字进行中文选择输入
                if LanguageUtil.detect_language() == "Chinese" and key.char.isdigit():
                    self.key_buffer.buf.clear()
                else:
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
                # 中文输入法时，输入中文后，按下空格应该清空缓冲区
                elif LanguageUtil.detect_language() == "Chinese" and key == Key.space:
                    self.key_buffer.buf.clear()
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
        # 监听鼠标事件
        self.mouse_hook()
        # 开启线程，监听键盘输入事件
        self.listener = keyboard.Listener(on_press=on_press, on_release=on_release)
        self.listener.start()

    def stop_hook(self):
        self.listener.stop()
        self.mouse_listener.stop()
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

    def mouse_hook(self):
        # 当鼠标按键按下时，不能确定位置处的数据，自动清除缓冲区数据
        def on_click(x, y, button, pressed):
            # 当鼠标按键被按下或释放时调用
            if button == mouse.Button.left:
                if pressed:
                    print(f"鼠标左键被按下, 清空buf")
                    self.key_buffer.buf.clear()

        self.mouse_listener = mouse.Listener(
            on_click=on_click,
        )
        self.mouse_listener.start()



if __name__ == "__main__":
    tmp = KeyHook()
    tmp.start_hook()
    while True:
        sleep(2)
        print(tmp.key_buffer.buf)


#