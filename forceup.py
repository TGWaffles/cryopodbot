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
r = praw.Reddit("Klok-Poster")
o = OAuth2Util.OAuth2Util(r)
o.refresh(force=True)
cryo = r.get_subreddit('thecryopodtohell')
upd = r.get_submission(url=str("https://www.reddit.com/r/klokscheduler/comments/5npysl/part_301/"))
totext = upd.selftext
totitle = upd.title
r.submit(cryo, totitle, totext)
