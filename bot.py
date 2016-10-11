#!/usr/bin/python
import praw
import pdb
import re
import time
#Imports all passwords from a hidden file ;)
from pw_bot import *
user_agent = ("CryoBot 1.0")
#Starts the main section of the reddit bot and assigns it to r.
r = praw.Reddit(user_agent = user_agent)
#Connects to the TCTH sub.
subreddit = r.get_subreddit("thecryopodtohell")
#Logs into Bot's Account from hidden file above.
r.login(REDDIT_USERNAME, REDDIT_PASS)
#for submission in subreddit.get_new(limit = 1):
#	author = submission.author
#	print(author)
#	time.sleep(5)
#	if str(author).lower() == "klokinator":
#		print("TEST!")
#		time.sleep(5)
		#if str(submission.title)[0:4].lower() == "part":
#Fetches all messages sent to the bot.
messages = r.get_inbox()
already_done = []
alreadyin = []
#For every message in the messages you just fetched:
for message in messages:
	#Open the username list
	file = open('list.txt', 'r+')
	#Add names from a username to a list and post ids to another.
	for line in file:
		linelen = len(line)
		newlinelen = linelen - 1
		if line[:newlinelen] not in alreadyin:
			alreadyin.append(line[:newlinelen])
	otherfile = open('done.txt', 'r+')
	for i in range(2):
		for line in otherfile:
			linelen = len(line)
			newlinelen = linelen - 1
			if line[:newlinelen] not in already_done:
				already_done.append(line[:newlinelen])
	#If the message talks about subscription, and if the author hasn't already been added and the id isn't done:
	if "subscribe" in str(message.body).lower() and str(message.author) not in alreadyin and str(message.id) not in already_done:
		#Double check to attempt to double-post proof.
		if str(message.author) not in alreadyin:
			#Write the sender's name in the username list.
			file.write("\n" + str(message.author))
			#Tells the sender they've been added.
			message.reply("BOT: Thanks, you've been added to the list!")
			time.sleep(2)
			#Adds their name to the ID list and stuff.
			alreadyin.append(message.author)
			already_done.append(message.id)
			otherfile.write("\n" + str(message.id))
	#Same as above but for unsubbing... Very system-intensive compared.
	elif "unsubscribe" in str(message.body).lower() and str(message.author) in alreadyin and str(message.id) not in already_done:
		f = open("list.txt","r+")
		d = f.readlines()
		f.seek(0)
		for i in d:
			if i != str(str(message.author) + "\n"):
				f.write(i)
		f.truncate()
		f.close()
	otherfile.close()
	file.close()
#Empty list to prevent double posts.
fixit = []
#For thread in the subreddit, out of the newest thread.
for submission in subreddit.get_new(limit=1):
	time.sleep(3)
	#Set variables to prevent annoying the reddit api.
	author = submission.author
	title = str(submission.title)
	id = str(submission.id)
	#Same as message checking but for threads.
	file = open('parts.txt','r+')
	for line in file:
		linelen = len(line)
		newlinelen = linelen - 1
		if line[:newlinelen] not in fixit:
			fixit.append(line)
	#If the author is Klok and it begins with part, do this:
	if str(author).lower() == "klokinator" and title[0:4].lower() == "part" and id not in fixit:
		file.write("\n" + id)
		time.sleep(5)
		file.close()
		file = open('list.txt', 'r+')
		alreadyin = []
		#Post the comment on the thread.
		postedcomment = submission.add_comment("Hi. I'm a bot, bleep bloop." + "\n" + "\n" + "If you're about to post regarding a typo and this Part was just posted, please wait ten minutes, refresh, and then see if it's still there!" + "\n" + "\n" + "Also, if you want to report typos anywhere, please respond to this bot to keep the main post clutter free. Thank you!" + "\n" + "\n" + "\n" + "[Click Here to be PM'd new updates!](https://np.reddit.com/message/compose/?to=CryopodBot&subject=Subscribe&message=Subscribe) " + "[Click Here to unsubscribe!](https://np.reddit.com/message/compose/?to=CryopodBot&subject=unsubscribe&message=unsubscribe)" + "\n" + "\n" + "\n" + "If you want to donate to Klokinator, send paypal gifts to Klokinator@yahoo.com, but be sure to mark it as a gift or Paypal takes 10%. " + "\n" + "\n" + "Patreon can also be pledged to [here!](https://www.patreon.com/klokinator)")
		#Sticky the comment that was just posted.
		postedcomment.distinguish(sticky=True)
		#Get the index list's ID.
		toedit = r.get_submission(submission_id='56tvbw')
		time.sleep(2)
		#Add post that was just posted to the index list.
		tempedit = toedit.selftext
		putin = tempedit + "\n" + "\n" + "[" + submission.title + "](" + submission.permalink + ")"
		time.sleep(2)
		toedit.edit(putin)
		time.sleep(2)
		#Put all users in the username file into a list, then:
		for line in file:
			linelen = len(line)
			newlinelen = linelen -1
			if line[:newlinelen] not in alreadyin:
				alreadyin.append(line[:newlinelen])
		#For every name in the list, send them this message with the link to the part.
		for name in alreadyin:
			r.send_message(name, "New Post!", "[New Post on /r/TheCryopodToHell!](" + submission.permalink + ")")
			time.sleep(5)
		file.close()
	else:
		file.close()
#Check & organise the username file for duplicates.
lines = open('list.txt', 'r').readlines()
lines_set = set(lines)
out  = open('list.txt', 'w')
for line in lines_set:
	out.write(line)
out.close()
