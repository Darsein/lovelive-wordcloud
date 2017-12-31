# -*- coding: utf-8 -*-

from collections import Counter
import argparse
from wordcloud import WordCloud
import os
import sys
import json
import random

def color_func_muse(word, font_size, position, orientation, random_state, font_path):
    return random.choice(['orange', 'deepskyblue', 'darkgrey', 'blue', 'yellow', 'red', 'darkviolet', 'limegreen', 'deeppink'])

def color_func_aqours(word, font_size, position, orientation, random_state, font_path):
    return random.choice(['darkorange', 'pink', 'lime', 'orangered', 'dodgerblue', 'lightgrey', 'gold', 'blueviolet', 'fuchsia'])

def multiply_counts(count_dict, ratio):
    for key in count_dict:
        count_dict [key] *= ratio;
    return count_dict

def create_wordcloud(frequency, output_path, colors):

    # 環境に合わせてフォントのパスを指定する。
    #fpath = "/System/Library/Fonts/HelveticaNeue-UltraLight.otf"
    fpath = "/Library/Fonts/ヒラギノ丸ゴ ProN W4.ttc"

    wordcloud = WordCloud(background_color="white",font_path=fpath, width=900, height=500,
    color_func=colors).fit_words(frequency)
    wordcloud.to_file(output_path)

def get_song_num(group_list):
    cnt = 0
    for group in group_list:
        dir_path = "word_count/" + group
        files = os.listdir(dir_path)
        for file in files:
            if file[0] == '.': continue
            cnt += 1
    return cnt

def get_word_counts(group_list, normalize):
    stop_words = {u'てる', u'する', u'なる', u'ん', u'の', u'いる', u'こと', u'れる',
     u'そう', u'みる', u'さ', u'いい', u'ある', u'それ', u'ない', u'よう', u'く', u'なさる'
     u'られる', u'どう', u'なん', u'せる', u't', u'やる', u'あう', u'よ', u'しまう', u'm'}
    total_word_counts = {}
    for group in group_list:
        dir_path = "word_count/" + group
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
                    total_word_counts[word] += 1 if normalize else int(count)

    return total_word_counts

def process(base_group_list, diff_group_list, title, normalize):
    word_counts = get_word_counts(base_group_list, normalize)

    if diff_group_list:
        base_word_counts = word_counts
        diff_word_counts = get_word_counts(diff_group_list, normalize)
        base_word_counts = multiply_counts(base_word_counts, get_song_num(diff_group_list))
        diff_word_counts = multiply_counts(diff_word_counts, get_song_num(base_group_list))

        filtered_word_counts = base_word_counts
        for word, count in diff_word_counts.items():
            if word in filtered_word_counts:
                filtered_word_counts[word] -= int(count)
                if filtered_word_counts[word] <= 0:
                    del filtered_word_counts[word]
        word_counts = filtered_word_counts

    color_func = None
    if base_group_list == ["muse"]:
        color_func = color_func_muse
    if base_group_list == ["aqours"]:
        color_func = color_func_aqours

    create_wordcloud(word_counts, "word_clouds/" + title + ".png", color_func)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Draw word cloud for the lyrics of the songs by given groups')
    parser.add_argument("-t", "--title", dest='title', metavar='TITLE', \
                        type=str, nargs='?', default="test", help='title for word cloud png file')
    parser.add_argument("-b", "--base_groups", dest='base_group_list', metavar='GROUP', \
                        type=str, nargs='*', default=["muse", "arise", "aqours", "saint_snow"], \
                        help='base groups for word cloud. Group names should be: "muse", "arise", "aqours", "saint_snow"')
    parser.add_argument("-d", "--diff_groups", dest='diff_group_list', metavar='GROUP', \
                        type=str, nargs='*', default=[], \
                        help='diff groups for word cloud. Group names should be: "muse", "arise", "aqours", "saint_snow"')
    parser.add_argument("-n", "--normalize", dest='normalize', action='store_true',
                        help='normalize word counts per song to 1')

    all_groups = ["muse", "arise", "aqours", "saint_snow"]
    args = parser.parse_args()
    base_group_list = args.base_group_list
    diff_group_list = args.diff_group_list

    unknown_base_groups = [g for g in base_group_list if not g in all_groups]
    if unknown_base_groups :
        sys.exit("Error: base groups contain unknown groups: " + ", ".join(unknown_base_groups))
    unknown_diff_groups = [g for g in diff_group_list if not g in all_groups]
    if unknown_diff_groups :
        sys.exit("Error: base groups contain unknown groups: " + ", ".join(unknown_diff_groups))

    process(base_group_list, diff_group_list, args.title, args.normalize)
