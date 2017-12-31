# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import time
import re
import sys
import urllib.request as urllib
import urllib.parse as urlparse
import urllib.error as urlerror
import json

def get_lyric_from_utaten(song_name, group, song_url):
    song_request = urllib.Request(song_url, headers={"User-Agent" : "Magic Browser"})
    try:
        song_htmldata = urllib.urlopen(song_request)
    except urlerror.URLError as e:
        print("failed to get a song page for " + song_name, e.reason)

    song = {}
    song_soup = BeautifulSoup(song_htmldata, "html.parser")
    contents_soup = song_soup.find("article", attrs={"class": "contentBox"})

    date_soup = contents_soup.find("div", attrs={"class": "contentBox__title"}).find("span", attrs={"style": "position: absolute; bottom: 4px; right: 4px; font-size: 14px; font-weight: bold;"})
    if date_soup :
        song["date"] = date_soup.string.strip().split()[0]
    else :
        song["date"] = ""

    work_soup = contents_soup.find("dl", attrs={"class": "lyricWork"})
    if work_soup :
        workers = work_soup.findAll("dd")
        song["writer"] = workers[0].string if len(workers) >= 1 else ""
        song["composer"] = workers[1].string if len(workers) >= 2 else ""
    else :
        song["writer"] = ""
        song["composer"] = ""

    lyric_body_soup = contents_soup.find("div", attrs={"class": "lyricBody"})
    if not lyric_body_soup :
        print("Lyric not available for " + song_name + "\n\n")
        return False
    lyric_soup = lyric_body_soup.find("div", attrs={"class": "medium"})
    for ruby in lyric_soup.findAll("span", attrs={"class": "rt"}) :
        ruby.decompose()
    for ruby in lyric_soup.findAll("span", attrs={"class": "ruby"}) :
        ruby.unwrap()
    for ruby in lyric_soup.findAll("span", attrs={"class": "rb"}) :
        ruby.unwrap()
    lyric = ""
    for string in lyric_soup.strings :
        lyric += string
    lyric = "\n".join(lyric.strip().split("\n")[:-1])
    song["lyric"] = lyric.strip()
    with open("lyrics/" + group["id"] + "/" + song_name + ".json", "w") as f:
        json.dump(song, f, ensure_ascii=False)
    return True

def get_lyric_from_anikashi(song_name, group, song_url):
    song_request = urllib.Request(song_url, headers={"User-Agent" : "Magic Browser"})
    try:
        song_htmldata = urllib.urlopen(song_request)
    except urlerror.URLError as e:
        print("failed to get a song page for " + song_name, e.reason)

    song = {}
    song_soup = BeautifulSoup(song_htmldata, "html.parser")
    row_soup = song_soup.find("table").findAll("td")
    date_match = re.search('(\d{4})年(\d{1,2})月(\d{1,2})日', row_soup[-1].string)
    if date_match :
        y, m, d = date_match.groups()
        song["date"] = "%s/%s/%s" % (y, m, d)

    # TODO: get writer and composer information
    song["writer"] = ""
    song["composer"] = ""

    lyric_soup = song_soup.find("div", attrs={"class": "kashitext"})
    lyric_soup.find("h2").decompose()
    for p_tag in lyric_soup.findAll("p") :
        p_tag.unwrap()
    for font_tag in lyric_soup.findAll("font") :
        font_tag.unwrap()
    lyric = ""
    for string in "".join(lyric_soup.strings).split("\n") :
        lyric += re.sub(r"^\(.*\) ", "", string)
    song["lyric"] = lyric.strip()

    with open("lyrics/" + group["id"] + "/" + song_name + ".json", "w") as f:
        json.dump(song, f, ensure_ascii=False)
    return True


def get_lyric_urls():
    utaten_url = "https://utaten.com"
    anikashi_url = "http://animationsong.com"

    groups = [ {"id": "muse", "name": "μ\'s"},
                {"id": "arise", "name": "A-RISE"},
                {"id": "aqours", "name": "Aqours"},
                {"id": "saint_snow", "name": "Saint Snow(Aqours)"}]
    song_list = {}
    for group in groups:
        with open("song_list/song_list_" + group["id"] + ".txt", "r") as f:
            for row in f:
                song_list[row[:-1]] = group

    for song_name, group in song_list.items():
        print(song_name, group["name"])
        # exceptions
        url_song_name = song_name
        if group["id"] == "muse" : url_song_name = song_name.replace("♡", " ")
        if url_song_name == "恋のシグナルRin rin rin!" : url_song_name = "恋のシグナルRin rin rin"
        if url_song_name == "君のこころは輝いてるかい？" : url_song_name = "君のこころは輝いてるかい"
        list_url = utaten_url + "/lyric/search?title=" + urlparse.quote_plus(url_song_name, encoding='utf-8')

        list_request = urllib.Request(list_url, headers={"User-Agent" : "Magic Browser"})
        try:
            list_htmldata = urllib.urlopen(list_request)
        except urllib.error.URLError as e:
            print("failed to get a list page for " + song_name, e.reason)

        list_soup = BeautifulSoup(list_htmldata, "html.parser")
        search_result_soup = list_soup.find("p", attrs={"class": "searchResult__title"})
        if search_result_soup :
            song_url = utaten_url + search_result_soup.find("a").get("href")
            if get_lyric_from_utaten(song_name, group, song_url) :
                continue

        list_url = anikashi_url + "/?s=" + urlparse.quote_plus(url_song_name, encoding='utf-8')
        list_request = urllib.Request(list_url, headers={"User-Agent" : "Magic Browser"})
        try:
            list_htmldata = urllib.urlopen(list_request)
        except urllib.error.URLError as e:
            print("failed to get a list page for " + song_name, e.reason)
        list_soup = BeautifulSoup(list_htmldata, "html.parser")
        search_result_soup = list_soup.find("h1", attrs={"class": "entry-title"})
        if search_result_soup :
            song_url = search_result_soup.find("a").get("href")
            if get_lyric_from_anikashi(song_name, group, song_url) :
                continue
        print(song_name + " not found in Uta-ten and Anikashi.\n\n")

def main():
    get_lyric_urls()

if __name__ == "__main__":
    if len(sys.argv) != 1:
        exit(1)
    main()
