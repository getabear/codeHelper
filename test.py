import time
import pyperclip
from pynput.keyboard import Controller, Key


def get_text_to_line_start():

    old_text = pyperclip.paste()

    # 创建键盘控制器
    keyboard = Controller()

    # 模拟按下 Shift + Home 键
    keyboard.press(Key.shift)
    keyboard.press(Key.home)
    keyboard.release(Key.home)
    keyboard.release(Key.shift)

    # 等待选择完成
    time.sleep(0.1)

    # 复制选中的文本
    keyboard.press(Key.ctrl_l)  # 对于 Windows 使用 Key.ctrl
    keyboard.press('c')
    keyboard.release('c')
    keyboard.release(Key.ctrl_l)

    # 等待粘贴操作完成
    time.sleep(0.1)

    # 消除选中
    keyboard.press(Key.right)
    keyboard.release(Key.right)

    # 从剪贴板获取文本
    text_to_line_start = pyperclip.paste()

    # 恢复剪切板数据
    pyperclip.copy(old_text)

    return text_to_line_start


