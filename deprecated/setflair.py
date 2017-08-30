#!/usr/bin/python
import praw
import pdb
import time
import re
from pw_bot import *
user_agent = ("CryoArchive Updater 1.0")
r = praw.Reddit(user_agent = user_agent)
subreddit = r.get_subreddit("thecryopodtohell")
r.login(REDDIT_USERNAME, REDDIT_PASS)
for submission in subreddit.get_new(limit=275):
	time.sleep(2)
	author = str(submission.author)
	title = str(submission.title)
	id = str(submission.id)
	if author.lower() == "klokinator" and title[0:4].lower() == "part":
		submission.set_flair("STORY", "story")
		time.sleep(2)
