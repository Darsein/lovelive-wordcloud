# -*- coding: utf-8 -*-

from collections import Counter
import os
import sys
import MeCab
import json

def mecab_analysis(text):
    mt = MeCab.Tagger('-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')
    node = mt.parseToNode(text)
    output = []
    while(node):
        if node.surface != "":  # ヘッダとフッタを除外
            word_type = node.feature.split(",")[0]
            if word_type in ["形容詞", "名詞", "副詞"]:
                output.append(node.surface)
            elif word_type == "動詞":
                output.append(node.feature.split(",")[6])
        node = node.next
        if node is None:
            break
    return output

def get_word_list():
    for group in ["muse", "arise", "aqours", "saint_snow"]:
        dir_path = "lyrics/" + group
        files = os.listdir(dir_path)
        for file in files:
            if file[0] == '.': continue
            with open(dir_path + "/" + file, "r") as input:
                lyric = json.load(input)["lyric"]
                word_dict = Counter(mecab_analysis(lyric))
                with open("word_count/" + group + "/" + file, "w") as output:
                    json.dump(word_dict, output, ensure_ascii=False)

def main():
    get_word_list()

if __name__ == "__main__":
    main()
