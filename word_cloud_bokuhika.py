# -*- coding: utf-8 -*-

import os
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import json
from wordcloud import WordCloud, ImageColorGenerator

def get_word_counts():
    stop_words = {u'てる', u'する', u'なる', u'ん', u'の', u'いる', u'こと', u'れる',
     u'そう', u'みる', u'さ', u'いい', u'ある', u'それ', u'ない', u'よう', u'く',
     u'られる', u'どう', u'なん', u'せる', u't', u'やる', u'あう', u'よ', u'しまう', u'm'}
    total_word_counts = {}
    dir_path = "word_count/muse"
    files = os.listdir(dir_path)
    for file in files:
        if file[0] == '.': continue
        with open(dir_path + "/" + file, "r") as f:
            word_counts = json.load(f)
            for word, count in word_counts.items():
                if word in stop_words:
                    continue
                if word not in total_word_counts:
                    total_word_counts[word] = 0
                total_word_counts[word] += int(count)

    return total_word_counts

def process():
    word_counts = get_word_counts()
    output_path = "bokuhika-wc.png"
    image = np.array(Image.open("bokuhika-color.png"))

    fpath = "/Library/Fonts/ヒラギノ丸ゴ ProN W4.ttc"
    image_colors = ImageColorGenerator(image)

    wc = WordCloud(background_color="white", mask=image, font_path=fpath, max_words=2000,
    max_font_size=80).fit_words(word_counts).recolor(color_func=image_colors).to_file(output_path)

if __name__ == "__main__":
    process()
