# #!/usr/bin/python
# import sys
# import logging
# import discord
# from discord.ext import commands
# import praw
# import pdb
# import re
# import time
# #Imports all passwords from a hidden file ;)
# from pw_bot import *
# logging.basicConfig(level=logging.INFO)
# donelist = []
# fulltext = ''
# currenttext = ''
# people = []
# statlist = []
# toreverse = []
# def statcheck():
	# file = open('statlines.txt', 'r+', encoding='palmos')
	# for line in file:
		# linelen = len(line)
		# newlinelen = linelen - 1
		# if line[:newlinelen] not in statlist:
			# statlist.append(line[:newlinelen])
	# file.close()
# def donecheck():
	# file = open('donestats.txt', 'r')
	# for line in file:
		# linelen = len(line)
		# newlinelen = linelen - 1
		# if line[:newlinelen] not in donelist:
			# donelist.append(line[:newlinelen])
	# file.close()
# statcheck()
# donecheck()
# user_agent = ("CryoStats 1.0")
# #Starts the main section of the reddit bot and assigns it to r.
# r = praw.Reddit(user_agent = user_agent)
# r.login(REDDIT_USERNAME, REDDIT_PASS)
# subreddit = r.get_subreddit("thecryopodtohell")
# for submission in subreddit.get_new(limit=500):
	# author = submission.author
	# title = str(submission.title)
	# print(title)
	# if str(author).lower() == "klokinator" and title[0:4].lower() == "part" and title not in toreverse:
		# toreverse.append(submission.title + "\n" + submission.selftext + "\n" + "\n")
# for i in toreverse:
	# file = open('full.txt', 'r')
	# for line in file:
		# currenttext = currenttext + line 
	# file.close()
	# file = open('full.txt', 'w')
	
# for i in reversed(toreverse):
	# file = open('full.txt', 'r')
	# for line in file:
		# currenttext = currenttext + line 
	# file.close()
	# file = open('reversedfull.txt', 'w')
	# file.write(currenttext + i)
	# print("Written!")
	# file.close()
# file.close()
# file = open('full.txt', 'r+')
# for line in file:
	# if line not in statlist:
		# f = open('chars.txt', 'r')
		# for line2 in f:
			# characters = int(line2)
			# print(line2)
		# f.close()
		# linelen = len(line)
		# newlinelen = linelen - 1
		# characters += newlinelen
		# f = open('chars.txt', 'w')
		# f.write(str(characters))
		# f.close()
		# fi = open('statlines.txt', 'r+')
		# fi.write(line + "\n")
		# fi.close()
		# statcheck()