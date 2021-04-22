#!/usr/bin/env python3
# -*- coding: utf-8 -*-

name = 'facebook_to_album'

from telegram_util import AlbumResult as Result

def dedup(images):
	exist = set()
	for image in images:
		if image in exist:
			continue
		if 'p32x32' in image:
			continue
		exist.add(image)
		yield image

def getText(text, comment):
	if not comment:
		return text
	index = comment.find('\n\n')
	if index == -1:
		return text
	comment = comment[index:].strip()
	if len(comment) < 10:
		return text
	if not text:
		return comment
	return text + '\n\ncomment: ' + comment
	
def get(content):
    result = Result()
    result.url = content['post_url']
    result.video = content['video']
    result.cap_html_v2 = getText(content['post_text'].strip(), content['shared_text'])
    result.imgs = list(dedup(content['images'] or []))
    return result