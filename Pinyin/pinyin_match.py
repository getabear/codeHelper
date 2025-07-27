from util import DictTree


# 将拼音存入字典树中，方便后续识别拼音
def init_dict_tree(dict_tree: DictTree):
    with open("pinyin.txt", "r", encoding='utf-8') as f:
        for line in f:
            # 将单词翻转，存入字典树中
            word = line[:-1][::-1]
            dict_tree.insert(word)



if __name__ == '__main__':
    tree = DictTree()
    init_dict_tree(tree)
    word = "ni"[::-1]
    print(tree.find(word))
