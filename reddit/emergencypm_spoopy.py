#!/usr/bin/python
import sys
import logging
import discord
import asyncio
import praw
import pdb
import re
import random
import time
from pw_bot import *
user_agent = ("CryoPMer 1.0")
r = praw.Reddit(user_agent = user_agent)
subreddit = r.get_subreddit("thecryopodtohell")
r.login(REDDIT_USERNAME, REDDIT_PASS)
file = open('list.txt', 'r+')
alreadyin = []
finished = []
todo = []
tosendtitle = str(input("What should the title be? "))
tosendpeople = str(input("What should we tell them? "))
for line in file:
	linelen = len(line)
	newlinelen = linelen -1
	if line[:newlinelen] not in alreadyin:
		alreadyin.append(line[:newlinelen])
#For every name in the list, send them this message with the link to the part.
for name in alreadyin:
	try:
		r.send_message(name, tosendtitle, tosendpeople)
		finished.append(str(name))
	except Exception as ex:
		print(ex)
		print(name)
		f = open('offenders.txt','r+')
		f.write(name + "\n")
		f.close()
	time.sleep(1)
time.sleep(10)
for line in file:
	linelen = len(line)
	newlinelen = linelen -1
	if line[:newlinelen] not in finished:
		todo.append(line[:newlinelen])
for name in todo:
	try:
		r.send_message(name, tosendpeople)
	except Exception as ex:
		print(ex)
		print(name)
		f = open('offenders.txt','r+')
		f.write(name + "\n")
		f.close()
		torem = name + "\n"
	time.sleep(1)
file.close()