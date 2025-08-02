import win32api, win32con, win32gui
import ctypes
from pynput.keyboard import Controller, Key

class LanguageUtil:
    def __init__(self):
        self.kc = Controller()

    def detect_language(self):
        IMC_GETOPENSTATUS = 0x0005
        IMC_SETOPENSTATUS = 0x0006

        imm32 = ctypes.WinDLL('imm32', use_last_error=True)
        handle = win32gui.GetForegroundWindow()	# 某进程窗口句柄
        hIME = imm32.ImmGetDefaultIMEWnd(handle)
        status = win32api.SendMessage(hIME, win32con.WM_IME_CONTROL, IMC_GETOPENSTATUS, 0)	# 返回值 0:英文 1:中文
        if status:
            return "Chinese"
        else:
            return "English"


    def change_language(self, language):
        cur_language = self.detect_language()
        if cur_language == language:
            return
        else:
            # 模拟用户按下切换输入法按键
            self.kc.press(Key.shift)
            self.kc.release(Key.shift)


if __name__ == '__main__':
    a = LanguageUtil()
    print(a.detect_language())
    import time
    time.sleep(1)
    a.change_language("Chinese")
