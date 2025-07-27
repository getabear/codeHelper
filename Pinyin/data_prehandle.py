import re

# 将拼音汉字的拼音提取出来，保存到pinyin.txt

def remove_tone_simple(pinyin):
    # 直接替换带音调的字符为无音标形式
    tone_map = {"ā": "a", "á": "a", "ǎ": "a", "à": "a",
                "ō": "o", "ó": "o", "ǒ": "o", "ò": "o",  # 重点替换 ò → o
                "ē": "e", "é": "e", "ě": "e", "è": "e",
                "ī": "i", "í": "i", "ǐ": "i", "ì": "i",
                "ū": "u", "ú": "u", "ǔ": "u", "ù": "u",
                "ǖ": "v", "ǘ": "v", "ǚ": "v", "ǜ": "v", "ü": "v"}
    return re.sub(r"[āáǎàōóǒòēéěèīíǐìūúǔùǖǘǚǜü]",
                 lambda m: tone_map[m.group(0)], pinyin)

pinyin = set()
with open("./kXHC1983.txt", "r", encoding='utf-8') as f:
    for line in f:
        res = re.search(r"\s([\S]+)\s*#", line)
        if res.group(1):
            item = remove_tone_simple(res.group(1))
            for word in item.split(','):
                pinyin.add(word)

with open("pinyin.txt", "w", encoding="utf-8") as f:
    for item in pinyin:
        f.write(item + "\n")
