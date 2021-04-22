#!/usr/bin/env python3
# -*- coding: utf-8 -*-

name = 'facebook_to_album'

from telegram_util import AlbumResult as Result

def dedup(images):
	exist = set()
	for image in images:
		if image in exist:
			continue
		exist.add(image)
		yield image

def getSharedText(text):
	if not text:
		return ''
	index = text.find('\n\n')
	return '\n\ncomment: ' + text[index:].strip()

def get(content):
    result = Result()
    result.url = content['post_url']
    result.cap_html_v2 = content['post_text'].strip() + getSharedText(content['shared_text'])
    result.imgs = list(dedup(content['images'] or []))
    return result