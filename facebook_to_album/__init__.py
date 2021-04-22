#!/usr/bin/env python3
# -*- coding: utf-8 -*-

name = 'rss_to_album'

from telegram_util import AlbumResult as Result
import yaml
import cached_url
from bs4 import BeautifulSoup, NavigableString
import feedparser

def getCap(soup):
    result = []
    for item in soup:
        if isinstance(item, NavigableString):
            text = item.strip()
            pieces = text.split()
            if pieces and pieces[0].startswith('@'):
                text = text.replace(pieces[0], '')
            if pieces and pieces[-1].startswith('@'):
                text = text.replace(pieces[-1], '')
            result.append(text.strip())
        elif item.name == 'br':
            result.append('\n')
        elif item.name not in ['img'] and '(Feed generated with FetchRSS)' != item.text:
            print(item.name, item.text.strip())
    return ''.join(result).strip()

def getImgs(soup):
    for item in soup.find_all('img'):
        yield item['src'].replace('&amp;', '&') 

def get(rss_path):
    feed = feedparser.parse(rss_path)
    feed_entries = feed.entries
    for entry in feed.entries:
        soup = BeautifulSoup(entry.description, 'html.parser')
        result = Result()
        result.url = entry.link
        result.cap_html_v2 = getCap(soup)
        result.imgs = list(getImgs(soup))
        # TODO: support video
        yield result