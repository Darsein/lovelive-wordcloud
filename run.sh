#!/bin/sh
set -e

mkdir lyrics
mkdir lyrics/muse
mkdir lyrics/arise
mkdir lyrics/aqours
mkdir lyrics/saint_snow
python get_lyrics_json.py

mkdir word_count
mkdir word_count/muse
mkdir word_count/arise
mkdir word_count/aqours
mkdir word_count/saint_snow
python lyric_to_words.py

mkdir word_clouds
python word_cloud.py
