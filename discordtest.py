import discord
import asyncio
import random
import time
import praw
from pw_bot import *
client = discord.Client()

@client.event
async def on_ready():
	print('LOGGED IN!')

@client.event
async def on_message(message):
	if message.content.startswith('!optin'):
		role = discord.utils.get(message.server.roles, name='@updaters')
		tmp = await client.send_message(message.channel, 'Trying to add you, @' + str(message.author))
		await client.add_roles(message.author, role)
		await client.edit_message(tmp, 'Added!')
		await asyncio.sleep(30)
		await client.delete_message(tmp)
		await client.delete_message(message)
	elif message.content.startswith('!optout'):
		role = discord.utils.get(message.server.roles, name='@updaters')
		tmp = await client.send_message(message.channel, 'Trying to remove you, @' + str(message.author))
		await client.remove_roles(message.author, role)
		await client.edit_message(tmp, 'Removed!')
		await asyncio.sleep(30)
		await client.delete_message(tmp)
		await client.delete_message(message)
async def new_part_checker():
	await client.wait_until_ready()
	user_agent = ("CryoChecker 1.0")
	r = praw.Reddit(user_agent = user_agent)
	r.login(REDDIT_USERNAME, REDDIT_PASS)
	subreddit = r.get_subreddit("thecryopodtohell")
	while True:
		fixit = []
		file = open('newpart.txt', 'r')
		for submission in subreddit.get_new(limit=1):
			author = submission.author
			title = str(submission.title)
			id = str(submission.id)
			file = open('donediscord.txt','r+')
			for line in file:
				linelen = len(line)
				newlinelen = linelen - 1
				if line[:newlinelen] not in fixit:
					fixit.append(line[:newlinelen])
			if str(author).lower() == "klokinator" and title[0:4].lower() == "part" and id not in fixit or str(author).lower() == "thomas1672" and title[0:4].lower() == "test" and id not in fixit:
				file.write(id + "\n")
				file.close()
				topost = "@everyone - " + title + " - <" + submission.permalink + ">"
				tmp = await client.send_message(client.get_channel('226088087996989450'), topost)
			else:
				file.close()
		await asyncio.sleep(15)
#async def reminder():
#	await client.wait_until_ready()
#	while True:
#		tmp = await client.send_message(client.get_channel('246162218104782848'), 'AUTOMATED MESSAGE: If you\'re not already subscribed on the discord, be sure to subscribe by doing !optin and if you feel the need to unsubscribe, just do !optout - in any chat! Also, here\'s some handy links:' + '\n' + 'Klok\'s Patreon: <https://www.patreon.com/klokinator>' + "\n" + 'My Github: <https://github.com/TGWaffles/cryopodbot>' + "\n" + 'Subreddit: <http://reddit.com/r/thecryopodtohell>')
#		await asyncio.sleep(21600)
#		await client.delete_message(tmp)
client.loop.create_task(new_part_checker())
#client.loop.create_task(reminder())
client.run(DISCORD_TOKEN)