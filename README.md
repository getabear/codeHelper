## 一个专为开发者设计的智能输入法，帮助你在编码过程中快速切换中英文输入和标点符号。

## ✨ 特性

- **智能拼音识别**：自动识别混合文本中的拼音并转换为中文
- **一键切换**：使用 f2: 键快速切换中英文和标点模式
- **开发者友好**：专为编码场景优化，不影响正常编程工作流
- **跨平台支持**：支持 Windows、macOS 和 Linux 系统

## 🚀 快速开始

```bash
git clone https://github.com/getabear/codeHelper.git
```

### 使用示例
可以自定义快捷键，只需将key_hook目录下的hotkeys中进行设置即可，这里以f2为例
```python

# 输入 "nihao" 后按 f2 键
输入: nihao 按键f2 → 输出: 你好
# 输入 "nihao" 后按 f2 键
输入: nihao 按键f2 → 输出: 你好

# 智能识别混合内容
输入: installnihao 按键f2 → 输出: install你好

# 中英文标点切换
中文模式: 你好。按键f2 → 输出: 你好.
英文模式: hello.按键f2 → 输出: hello。
```

## 🙏 致谢
- 感谢 [pinyin](https://github.com/mozillazg/python-pinyin) 库提供的拼音文件
- 感谢pynput库提供的键盘监听库

  
