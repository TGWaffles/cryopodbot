import praw
import OAuth2Util
import sys
import logging
import discord
import asyncio
import praw
import pdb
import re
import random
import time
print("Started!")
print("1")
logging.basicConfig(level=logging.INFO)
from datetime import datetime
from threading import Timer
r = praw.Reddit("Klok-Poster")
o = OAuth2Util.OAuth2Util(r)
o.refresh(force=True)
print("1")
subreddit = r.get_subreddit('klokscheduler')
x=datetime.today()
fixit = []
print("1")
print(str(datetime.now().hour))
def postpart(po, secs):
	try:
		cryo = r.get_subreddit('thecryopodtohell')
		time.sleep(secs)
		upd = r.get_submission(url=str(po.permalink))
		totext = upd.selftext
		totitle = upd.title
		postedpart = r.submit(cryo, totitle, totext)
		print("1")
		po.delete()
	except Exception as e:
		file = open('error.txt','r+')
		file.write(str(e))
		file.close()
print("1")
for submission in subreddit.get_new(limit=1):
	print("1")
	author = submission.author
	title = str(submission.title)
	id = str(submission.id)
	file = open('parts.txt','r+')
	for line in file:
		linelen = len(line)
		newlinelen = linelen - 1
		if line[:newlinelen] not in fixit:
			fixit.append(line[:newlinelen])
	file.seek(0)
	file.close()
	if str(author).lower() == "klokinator" and title[0:4].lower() == "part" and id not in fixit or str(author).lower() == "thomas1672" and title[0:4].lower() == "test" and id not in fixit:
		print("FOUND")
		file = open('parts.txt','r+')
		file.write(id + "\n")
		file.close()
		try:
			print("TRYING")
			tz = submission.comments[0]
			tz1 = tz.body
			tz2 = int(tz1) + 3
			print("TIME: " + str(tz2))
			totitle = title
			totext = submission.selftext
			now = datetime.now()
			if int(now.hour) > tz2:
				hours = int(24 + tz2) - int(now.hour)
				mins = hours * 60 - now.minute
				secs = int(mins) * 60
				tz.reply("Set for the time: " + str(tz1) + " on: " + str(x.day) + "/" + str(now.month))
			else:
				mleft = now.minute
				print("CURRENT TIME: " + str(now.hour))
				print("CURRENT - TODO = " + str(int(tz2 - int(now.hour))))
				mins = int(tz2 - int(now.hour)) * 60 - mleft
				secs = int(mins) * 60
				tz.reply("Set for the time: " + str(tz1) + " on: " + str(x.day) + "/" + str(now.month))
			print(str(secs))
			postpart(submission, secs)
		except Exception as e:
			print(str(e))