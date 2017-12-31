# coding:utf-8

import requests
import sys
import json
import os
import re
import urllib2
from bs4 import BeautifulSoup
from datetime import date

NHK_NEWS_LIST_JSON = "http://www3.nhk.or.jp/news/easy/news-list.json"


def parse(target_url, output_folder):
    list_json = requests.get(NHK_NEWS_LIST_JSON)
    list_json.encoding = 'utf-8-sig'
    nhk_news = json.loads(list_json.text)

    news_id = re.search()

    # make output dir
    if os.path.isdir(output_folder) == False:
        os.makedirs(output_folder)

    # get data from nhk news json
    news = None
    for k, v in nhk_news[0].items():
        for m in v:
            if m['news_id'].encode('utf8') == target_url:
                news = m
                break

    if news is None:
        print "There is no news on nhk"
        return

    # parse news
    parse_news(news, output_folder)


def parse_news(news, output_folder):
    news_id = news['news_id']
    news_time = news['news_prearranged_time'].replace(':', '-')
    title = news['title']
    title_ruby = news['title_with_ruby']
    news_uri = 'http://www3.nhk.or.jp/news/easy/' + str(news_id) + '/' + str(news_id) + '.html'
    voice_uri = 'http://www3.nhk.or.jp/news/easy/'

    r = requests.get(news_uri)
    r.encoding = 'utf-8'

    soup = BeautifulSoup(r.text, 'html.parser')
    date = soup.find('p', attrs={'id': 'newsDate'}).contents[0]
    title = soup.find('div', attrs={'id': 'newstitle'})
    article = soup.find('div', attrs={'id': 'newsarticle'})

    # write html
    output = os.path.join(output_folder, "artcile.html")
    with open(output, "w") as f:
        print >> f, '<?xml version="1.0" encoding="UTF-8" ?>'
        print >> f, "<!DOCTYPE html>"
        print >> f, "<html lang='ja'>"
        print >> f, '<head><meta http-equiv="content-type" content=application/xhtml+xml; charset=UTF-8" >'
        print >> f, '<style type="text/css">body { margin-left: 1em; margin-right: 1em; } {font-family: serif;} p { text-indent: 1em;} h2{ font-size: large; font-weight: bold;}</style>'
        print >> f, "</head>"
        print >> f, "<body>"
        print >> f, "<br />".join([str(title), str(article)])
        print >> f, "</body>"
        print >> f, "</html>"
        print("File \"" + output + "\" created")

    print("The month's news were downloaded from NHK.")

    # write audio
    if news["has_news_easy_voice"] == True:
        voice_uri = "%s/%s/%s" % (voice_uri, news["news_id'"], news["news_easy_voice_uri"])
        urllib2.urlretrieve(voice_uri, os.path.join(output_folder, news["news_easy_voice_uri"]))

    # write video
    if news["has_news_easy_voice"] == True:
        voice_uri = "%s/%s/%s" % (voice_uri, news["news_id'"], news["news_easy_voice_uri"])
        urllib2.urlretrieve(voice_uri, os.path.join(output_folder, news["news_easy_voice_uri"]))


        # write image


def main():
    target_url = "http://www3.nhk.or.jp/news/easy/k10011268561000/k10011268561000.html"
    output_folder = "/Users/gaobester/WorkSpace/NHKNews/zhizhu/output"

    parse(target_url, output_folder)


main()
