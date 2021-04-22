#!/usr/bin/env python3
# -*- coding: utf-8 -*-

name = 'facebook_to_album'

from telegram_util import AlbumResult as Result

def get(content):
    result = Result()
    result.url = content['post_url']
    result.cap_html_v2 = content['text']
    result.imgs = content['images']
    return result