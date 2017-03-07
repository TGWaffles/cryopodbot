#Imports all the functions useful for the bot.
import discord
import asyncio
import random
import requests
import re
import os
import psutil
import time
import aiohttp
import math
import praw
from pw_bot import *
#Defines info about the bot and regular PRAW info for reddit post-grabbing.
client = discord.Client()
user_agent = ("CryoChecker 1.0")
r = praw.Reddit(user_agent = user_agent)
r.login(REDDIT_USERNAME, REDDIT_PASS)
subreddit = r.get_subreddit("thecryopodtohell")
r.config.store_json_result = True
@client.event
async def on_ready():
	print('LOGGED IN!')
client.aiosession = aiohttp.ClientSession(loop=client.loop)
global enabled
enabled = 0
global apenabled
apenabled = 0
async def uwordcount(text):
	uwc = []
	wc = 0
	for i in str(text).split():
		if i not in uwc:
			wc += 1
			uwc.append(i)
	return wc
async def discordify(fullmessage, mesc, append="", character_limit=2000, deletemess=False, deletetime=0, delay=False):
	messages = []
	tempmessage = fullmessage
	while len(tempmessage) > character_limit:
		split_index = tempmessage[:character_limit].rfind("\n")
		if split_index == -1:
			# No space found, just split at the character limit
			split_index = tempmessage[:character_limit].rfind(" ")
			if split_index == -1:
				split_index = character_limit
			else:
				split_index += 1
		else:
			# Else space is found, split after the space
			split_index += 1
		messages.append(tempmessage[:split_index])
		tempmessage = tempmessage[split_index:]
	if len(tempmessage) > 1950:
		messages.append(tempmessage)
		messages.append(append)
	else:
		messages.append(tempmessage + append)
	for i in messages:
		tmp = await client.send_message(mesc, i)
		if deletemess == True:
			client.loop.create_task(delete_this_message(tmp, deletetime))
		if delay == True:
			await asyncio.sleep(2)
@client.event
async def on_message(message):
	if message.content.startswith('!optin'):
		role = discord.utils.get(message.server.roles, name='@updaters')
		tmp = await client.send_message(message.channel, 'Trying to add you, @' + str(message.author.mention))
		await client.add_roles(message.author, role)
		await client.edit_message(tmp, 'Added!')
		await asyncio.sleep(30)
		await client.delete_message(tmp)
		await client.delete_message(message)
	elif message.content.startswith('!optout'):
		role = discord.utils.get(message.server.roles, name='@updaters')
		tmp = await client.send_message(message.channel, 'Trying to remove you, @' + str(message.author.mention))
		await client.remove_roles(message.author, role)
		await client.edit_message(tmp, 'Removed!')
		await asyncio.sleep(30)
		await client.delete_message(tmp)
		await client.delete_message(message)
	# elif message.content.startswith('!uclean'):
		# counter = 0
		# server = client.get_server('226084200405663754')
		# utoclean = server.get_member_named(str(message.content).split(" ")[1])
		# atoclean = int(str(message.content).split(" ")[2])
		# print("Amount: " + str(atoclean))
		# print("User: " + str(utoclean))
		# if str(message.author).lower() == "tgwaffles#5354" or str(message.author).lower() == "klokinator#0278":
			# tmp = await client.send_message(message.channel, "Working on it!")
			# async for log in client.logs_from(message.channel, limit=int(atoclean + 1)):
				# print(log.content)
				# if log.author == utoclean:
					# await client.delete_message(log)
					# print("Deleting a message!")	
					# counter += 1
			# await client.edit_message(tmp, "Done cleaning, " + str(message.author.mention) + "!" + " I cleaned up " + str(counter) + " messages!")
			# await asyncio.sleep(30)
			# await client.delete_message(tmp)
	elif message.content.startswith('!say'):
		tosay = str(message.content)[4:]
		channel = message.channel
		author = str(message.author)
		await client.delete_message(message)
		if author.lower() == "tgwaffles#5354":
			tmp = await client.send_message(channel, str(tosay))
			await asyncio.sleep(60)
			await client.delete_message(tmp)
	elif message.content.startswith('!avatar') and str(message.author).lower() == "fawful#9748" or message.content.startswith('!avatar') and str(message.author).lower() == "tgwaffles#5354":
		if message.attachments:
			thing = message.attachments[0]['url']
		else:
			url = message.content[4:]
			thing = url.strip('<>')
		async with client.aiosession.get(thing) as res:
			await client.edit_profile(avatar=await res.read())
			tmp = await client.send_message(message.channel, "Done it for you, master " + str(message.author.mention))
			await asyncio.sleep(30)
			await client.delete_message(tmp)
	elif message.content.startswith('!newpart'):
		print("Message author: " + str(message.author) + " Says: " + str(message.content))
		if message.server == client.get_server('226084200405663754'):
			readit = []
			file = open('donediscord.txt', 'r')
			for line in file:
				linelen = len(line)
				newlinelen = linelen - 1
				if line[:newlinelen] not in readit:
					readit.append(line[:newlinelen])
			file.close()
			subidt = readit[-1]
			if subidt[-2:] == "\n":
				subid = str(subidt)[:-2]
			else:
				subid = subidt
			post = r.get_submission(submission_id=subid)
			text = str(post.selftext)
			uwc = []
			wc = 0
			for i in str(post.selftext).split():
				if i not in uwc:
					wc += 1
					uwc.append(i)
			fulltosay = str(post.title) + "\n" + str(post.permalink) + "\n" + "Wordcount of this part was: " + str(len(str(post.selftext).split())) + ", the character count was: " + str(len(str(text))) + " and the unique word count was: " + str(wc)
			tmp = await client.send_message(message.channel, fulltosay)
			await asyncio.sleep(120)
			await client.delete_message(tmp)
			await client.delete_message(message)
		else:
			readit = []
			file = open('donediscord.txt', 'r')
			for line in file:
				linelen = len(line)
				newlinelen = linelen - 1
				if line[:newlinelen] not in readit:
					readit.append(line[:newlinelen])
			file.close()
			subidt = readit[-1]
			if subidt[-2:] == "\n":
				subid = str(subidt)[:-2]
			else:
				subid = subidt
			post = r.get_submission(submission_id=subid)
			text = str(post.selftext)
			title = await client.send_message(message.channel, str(post.title))
			append = "\n" + "Wordcount of this part was: " + str(len(str(post.selftext).split())) + ", the character count was: " + str(len(str(post.selftext))) + " and the unique word count was: " + str(await uwordcount(post.selftext))
			client.loop.create_task(discordify(text, message.channel, append))
	elif message.content.startswith('!part'):
		found = False
		print("Message author: " + str(message.author) + " Says: " + str(message.content))
		number = str(message.content).split()[1]
		query = "Part " + number
		if message.server == client.get_server('226084200405663754'):
			for submission in r.search(str(query), subreddit='thecryopodtohell'):
				if found == False:
					author = submission.author
					title = str(submission.title)
					id = str(submission.id)
					if str(author).lower() == "klokinator" and title.startswith(query):
						post = submission
						text = str(post.selftext)
						uwc = []
						wc = 0
						for i in str(post.selftext).split():
							if i not in uwc:
								wc += 1
								uwc.append(i)
						fulltosay = str(post.title) + "\n" + str(post.permalink) + "\n" + "Wordcount of this part was: " + str(len(str(post.selftext).split())) + ", the character count was: " + str(len(str(text))) + " and the unique word count was: " + str(wc)
						tmp = await client.send_message(message.channel, fulltosay)
						await asyncio.sleep(120)
						await client.delete_message(tmp)
						await client.delete_message(message)
						found = True
		else:
			for submission in r.search(str(query), subreddit='thecryopodtohell'):
				if found == False:
					author = submission.author
					title = str(submission.title)
					id = str(submission.id)
					if str(author).lower() == "klokinator" and title.startswith(query):
						post = submission
						text = str(post.selftext)
						title = await client.send_message(message.channel, str(post.title))
						append = "\n" + "Wordcount of this part was: " + str(len(str(post.selftext).split())) + ", the character count was: " + str(len(str(post.selftext))) + " and the unique word count was: " + str(await uwordcount(post.selftext))
						client.loop.create_task(discordify(text, message.channel, append))
						found = True
	elif message.content.startswith('!stats'):
		global enabled
		global stat
		global totups
		global totproc
		global totrat
		global totwc
		global totuwc
		global totcc
		global biggestpart
		global biggesttitle
		global enabled
		global finished
		global stat
		global append
		global ehashappened
		global errmsg
		global tosenderr
		ehashappened = False
		if enabled == 0:
			enabled = 1
			finished = 0
			if str(message.author).lower() == "tgwaffles#5354" or str(message.author).lower() == "klokinator#0278":
				print(str(message.content))
				stat = ""
				totups = 0
				totproc = 0
				totrat = 0
				totwc = 0
				totuwc = 0
				totcc = 0
				biggestpart = 0
				biggesttitle = ""
				tmp = await client.send_message(message.channel, "Starting statter now! Processed: 0")
				for submission in subreddit.get_new(limit=750):
					author = submission.author
					title = str(submission.title)
					id = str(submission.id)
					if title.startswith('Part') and str(author).lower() == "klokinator":
						try:
							url = submission.permalink
							html = str(requests.get(url,headers = {'User-agent':'...'}).content)
							try:
								ratio = re.findall(';\((.*?)% upvoted\)',html)[0]
							except Exception as e:
								print(e)
								ratio = float(totrat / totproc)
							wordcount = str(len(str(submission.selftext).split()))
							charcount = str(len(str(submission.selftext)))
							unwordcount = str(await uwordcount(submission.selftext))
							stat = title + ": Upvotes: " + str(submission.ups) + ", Ratio: " + str(ratio) + "%" + ", Wordcount: " + str(wordcount) + ", Character Count: " + str(charcount) + ", Unique Wordcount: " + str(unwordcount) + "\n" + str(stat)
							totups += int(submission.ups)
							totproc += 1
							totrat += int(ratio)
							totwc += int(wordcount)
							totuwc += int(unwordcount)
							totcc += int(charcount)
							if int(charcount) > biggestpart:
								biggestpart = int(charcount)
								biggesttitle = title
							print(str(totproc))
							await client.edit_message(tmp, "Starting statter now! Processed: " + str(totproc) + ", current CPU usage: " + str(psutil.cpu_percent(interval=None)) + "%")
							await asyncio.sleep(0.25)
						except Exception as e:
							print(e)
							if ehashappened == False:
								tosenderr = "Error has occurred! Beginning error message!" + "\n" + "\n" + "```" + title + " : " + e + "```"
								errmsg = await client.send_message(message.channel, tosenderr)
								ehashappened = True
							else:
								lento = len(tosenderr)
								newlen = lento - 4
								tosenderr = tosenderr[:newlen] + "\n" + title + " : " + e + "```"
								await client.edit_message(errmsg, tosenderr)
				append = "\n" + "Total upvotes: " + str(totups) + ", total submissions processed: " + str(totproc) + ", average upvotes per submission: " + str(round(float(totups / totproc), 2)) + ", average upvote ratio: " + str(round(float(totrat / totproc), 2)) + "%" + ", total wordcount: " + str(totwc) + ", total character count: " + str(totcc) + ", total unique wordcount: " + str(totuwc) + ", average wordcount: " + str(round(float(totwc / totproc), 2)) + ", average character count: " + str(round(float(totcc / totproc), 2)) + ", average unique wordcount (per-post): " + str(round(float(totuwc / totproc), 2)) + ", largest part: " + str(biggesttitle) + " kloking in at over " + str(biggestpart) + " characters!"
				client.loop.create_task(discordify(stat, message.channel, append, deletemess=True, deletetime=600, character_limit=1900, delay=True))
				finished = 1
				enabled = 0
				await asyncio.sleep(30)
				await client.delete_message(tmp)
			elif message.server == client.get_server('226084200405663754'):
				tmp = await client.send_message(message.channel, "Not in this channel, " + str(message.author.mention) + "!")
				await asyncio.sleep(30)
				await client.delete_message(tmp)
			else:
				print(str(message.content))
				stat = ""
				totups = 0
				totproc = 0
				totrat = 0
				totwc = 0
				totuwc = 0
				totcc = 0
				biggestpart = 0
				biggesttitle = ""
				tmp = await client.send_message(message.channel, "Starting statter now! Processed: 0")
				for submission in subreddit.get_new(limit=750):
					author = submission.author
					title = str(submission.title)
					id = str(submission.id)
					if title.startswith('Part') and str(author).lower() == "klokinator":
						url = submission.permalink
						html = str(requests.get(url,headers = {'User-agent':'...'}).content)
						ratio = re.findall(';\((.*?)% upvoted\)',html)[0]
						wordcount = str(len(str(submission.selftext).split()))
						charcount = str(len(str(submission.selftext)))
						unwordcount = str(await uwordcount(submission.selftext))
						stat = title + ": Upvotes: " + str(submission.ups) + ", Ratio: " + ratio + "%" + ", Wordcount: " + wordcount + ", Character Count: " + charcount + ", Unique Wordcount: " + unwordcount + "\n" + stat
						totups += int(submission.ups)
						totproc += 1
						totrat += int(ratio)
						totwc += int(wordcount)
						totuwc += int(unwordcount)
						totcc += int(charcount)
						if int(charcount) > biggestpart:
							biggestpart = int(charcount)
							biggesttitle = title
						print(str(totproc))
						await client.edit_message(tmp, "Starting statter now! Processed: " + str(totproc) + ", current CPU usage: " + str(psutil.cpu_percent(interval=None)) + "%")
						await asyncio.sleep(0.25)
				append = "\n" + "Total upvotes: " + str(totups) + ", total submissions processed: " + str(totproc) + ", average upvotes per submission: " + str(round(float(totups / totproc), 2)) + ", average upvote ratio: " + str(round(float(totrat / totproc), 2)) + "%" + ", total wordcount: " + str(totwc) + ", total character count: " + str(totcc) + ", total unique wordcount: " + str(totuwc) + ", average wordcount: " + str(round(float(totwc / totproc), 2)) + ", average character count: " + str(round(float(totcc / totproc), 2)) + ", average unique wordcount (per-post): " + str(round(float(totuwc / totproc), 2)) + ", largest part: " + str(biggesttitle) + " kloking in at over " + str(biggestpart) + " characters!"
				client.loop.create_task(discordify(stat, message.channel, append, deletemess=True, deletetime=600, character_limit=1900))
				finished = 1
				enabled = 0
		else:
			if message.server != client.get_server('226084200405663754'):
				tmp = await client.send_message(message.channel, "Starting statter now! Processed: " + str(totproc))
				while finished == 0:
					await client.edit_message(tmp, "Starting statter now! Processed: " + str(totproc))
					await asyncio.sleep(0.25)
				client.loop.create_task(discordify(stat, message.channel, append, deletemess=True, deletetime=600, character_limit=1900))
	elif message.content.startswith('!cancel'):
		if str(message.author).lower() == "tgwaffles#5354":
			tmp = await client.send_message(message.channel, "ATTEMPTING TO CANCEL ALL RUNNING TASKS!")
			try:
				delete_this_message.cancel()
				self_cleaner.cancel()
				discordify.cancel()
				uwordcount.cancel()
				await client.edit_message(tmp, "CANCELLED ALL OTHER RUNNING TASKS. CANCELLING MYSELF NOW. IF THERE IS NO RESPONSE FROM HERE, ASSUME I CANCELLED MYSELF SUCCESSFULLY.")
				on_message.cancel()
			except Exception as e:
				await client.edit_message(tmp, "Sorry, boss... I failed. Here's my exception...: " + str(e))
		else:
			tmp = await client.send_message(message.channel, "Pfft, no.")
			await asyncio.sleep(30)
			await client.delete_message(tmp)
	#Code for changing my role's colour!
	elif message.content.startswith('!colour'):
		if str(message.author).lower() == "tgwaffles#5354":
			brole = discord.utils.get(client.get_server('226084200405663754').roles, name='Bot')
			bcol = brole.colour
			erole = discord.utils.get(client.get_server('226084200405663754').roles, name='@everyone')
			ecol = erole.colour
			curole = discord.utils.get(client.get_server('226084200405663754').roles, name='Bot Dev')
			cucol = curole.colour
			if cucol == bcol:
				await client.edit_role(client.get_server('226084200405663754'), curole, colour=ecol)
			else:
				await client.edit_role(client.get_server('226084200405663754'), curole, colour=bcol)
	elif message.content.startswith('!reboot'):
		if str(message.author).lower() == "tgwaffles#5354" or str(message.author).lower() == "klokinator#0278":
			tmp = await client.send_message(message.channel, "Restarting!")
			os.system('shutdown -r -t now now')
			await asyncio.sleep(5)
			await client.edit_message(tmp, "Reboot failed!")
		else:
			tmp = await client.send_message(message.channel, "Heh... No perms, I see? Not happening :)")
			await asyncio.sleep(20)
			await client.delete_message(tmp)
			await client.delete_message(message)
	elif message.content.startswith('!allparts'):
		global apenabled
		global aptotproc
		global aptosend
		global apappend
		global apfinished
		aptosend = ""
		if apenabled == 0:
			apenabled = 1
			apfinished = 0
			aptotproc = 0
			if message.server != client.get_server('226084200405663754'):
				tmp = await client.send_message(message.channel, "Starting partfinder now! Processed: 0")
				tosend = ""
				for submission in subreddit.get_new(limit=750):
					author = submission.author
					title = str(submission.title)
					id = str(submission.id)
					if title.startswith('Part') and str(author).lower() == "klokinator":
						aptosend = "~~                                                                                                                                                                                                                                        ~~" + title + "\n" + str(submission.selftext) + "\n" + "\n" + aptosend
						aptotproc += 1
					await client.edit_message(tmp, "Starting partfinder now! Processed: " + str(aptotproc) + ", current CPU usage: " + str(psutil.cpu_percent(interval=None)) + "%")
					await asyncio.sleep(0.5)
				apappend = "\n" + "\n" + "That took me a long time. You should be grateful."
				client.loop.create_task(discordify(aptosend, message.channel, apappend))
				apfinished = 1
				apenabled = 0
		else:
			if message.server != client.get_server('226084200405663754'):
				tmp = await client.send_message(message.channel, "Starting partfinder now! Processed: " + str(aptotproc) + ", current CPU usage: " + str(psutil.cpu_percent(interval=None)) + "%")
				while apfinished == 0:
					await client.edit_message(tmp, "Starting partfinder now! Processed: " + str(aptotproc))
					await asyncio.sleep(0.25)
				client.loop.create_task(discordify(aptosend, message.channel, apappend))
	elif message.content.startswith('!selfclean'):
		if str(message.author).lower() == "tgwaffles#5354":
			client.loop.create_task(self_cleaner())
async def new_part_checker():
	await client.wait_until_ready()
	while True:
		try:
			fixit = []
			for submission in subreddit.get_new(limit=3):
				author = submission.author
				title = str(submission.title)
				id = str(submission.id)
				file = open('donediscord.txt','r+')
				for line in file:
					linelen = len(line)
					newlinelen = linelen - 1
					if line[:newlinelen] not in fixit:
						fixit.append(line[:newlinelen])
				if str(author).lower() == "klokinator" and title.lower().startswith('part') and id not in fixit: #or str(author).lower() == "thomas1672" and title[0:4].lower() == "test" and id not in fixit:
					file.write(id + "\n")
					file.close()
					uwc = []
					wc = 0
					for i in str(submission.selftext).split():
						if i not in uwc:
							wc += 1
							uwc.append(i)
					topost = "@everyone - " + title + " - <" + submission.permalink + ">" + " Wordcount of this part: " + str(len(str(submission.selftext).split())) + ", character count: " + str(len(str(submission.selftext))) + " unique word count: " + str(wc)
					tmp = await client.send_message(client.get_channel('226088087996989450'), topost)
				else:
					file.close()
			await asyncio.sleep(15)
		except Exception as e:
			print(e)
async def delete_this_message(mess, whento=0):
	await asyncio.sleep(whento)
	await client.delete_message(mess)
async def self_cleaner():
	await client.wait_until_ready()
	while True:
		counter = 0
		channels = ['229813048905302017','226084200405663754']
		for i in channels:
			async for log in client.logs_from(client.get_channel(i), limit=500):
				if log.author == client.user:
					await client.delete_message(log)
					print("Deleting a message!")
					counter += 1
				elif log.content.startswith('!'):
					await client.delete_message(log)
					counter += 1
		print("Done cleaning, " + "! I cleaned up " + str(counter) + " messages!")
		await asyncio.sleep(2000)
async def game_updater():
	await client.wait_until_ready()
	while True:
		await client.change_presence(game=discord.Game(name=str(psutil.cpu_percent(interval=None)) + "% CPU Usage!"))
		await asyncio.sleep(2)
#async def reminder():
#	await client.wait_until_ready()
#	while True:
#		tmp = await client.send_message(client.get_channel('246162218104782848'), 'AUTOMATED MESSAGE: If you\'re not already subscribed on the discord, be sure to subscribe by doing !optin and if you feel the need to unsubscribe, just do !optout - in any chat! Also, here\'s some handy links:' + '\n' + 'Klok\'s Patreon: <https://www.patreon.com/klokinator>' + "\n" + 'My Github: <https://github.com/TGWaffles/cryopodbot>' + "\n" + 'Subreddit: <http://reddit.com/r/thecryopodtohell>')
#		await asyncio.sleep(21600)
#		await client.delete_message(tmp)
client.loop.create_task(new_part_checker())
client.loop.create_task(game_updater())
client.loop.create_task(self_cleaner())
#client.loop.create_task(reminder())
client.run(DISCORD_TOKEN)