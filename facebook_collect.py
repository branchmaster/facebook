#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import yaml
from telegram_util import log_on_fail
from telegram.ext import Updater
import plain_db
import cached_url
from bs4 import BeautifulSoup
import album_sender
import time
import facebook_to_album


with open('credential') as f:
	credential = yaml.load(f, Loader=yaml.FullLoader)

with open('db/setting') as f:
	setting = yaml.load(f, Loader=yaml.FullLoader)

existing = plain_db.loadKeyOnlyDB('existing')
tele = Updater(credential['bot_token'], use_context=True)
debug_group = tele.bot.get_chat(credential['debug_group'])

@log_on_fail(debug_group)
def run():
	sent = False
	for channel_id, detail in setting.items():
		channel = tele.bot.get_chat(channel_id)
		for name, rss in detail.items():
			for album in rss_to_album.get(rss):
				if existing.contain(album.url):
					continue
				if not sent:
					sent = True
				else:
					item_len = len(album.imgs) or 1
					time.sleep(item_len * item_len + 5 * item_len)
				album_sender.send_v2(channel, album)
				existing.add(album.url)
		
if __name__ == '__main__':
	run()