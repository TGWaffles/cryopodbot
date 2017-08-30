import asyncio
import string
import aiohttp
import discord
import os
import psutil
import re
from discord.ext import commands
from discutils import RThreadWrapper, Vars, uwordcount, permcheck, owners
from pw_bot import *


class CryopodBot:
    bot = commands.Bot(
        command_prefix = '!',
        description = 'Cryopodbot'
    )

    def __init__(self):

        # klok's and tg's ids, respectively
        # better than keeping two Member objects
        self.owners = owners

        # praw magical thread magic
        self.r = RThreadWrapper()

        # a class to hold all tg's precious global variables
        self.v = Vars()

        # aiohttp session for magix
        self.session = aiohttp.ClientSession()

    # ===============
    # bot commands
    # ===============
    @bot.command(pass_context = True)
    async def optout(self, ctx):
        role = discord.utils.get(ctx.message.server.roles, name = '@updaters')
        tmp = await self.bot.say('Trying to remove you, ' + str(ctx.message.author.mention))
        await self.bot.remove_roles(ctx.message.author, role)
        await self.bot.edit_message(tmp, 'Removed!')
        await asyncio.sleep(30)
        await self.bot.delete_message(tmp)
        await self.bot.delete_message(ctx.message)

    @bot.command(pass_context = True)
    async def optin(self, ctx):
        role = discord.utils.get(ctx.message.server.roles, name = '@updaters')
        tmp = await self.bot.say('Trying to add you, ' + str(ctx.message.author.mention))
        await self.bot.add_roles(ctx.message.author, role)
        await self.bot.edit_message(tmp, 'Added!')
        await asyncio.sleep(30)
        await self.bot.delete_message(tmp)
        await self.bot.delete_message(ctx.message)

    @bot.command(pass_context = True)
    async def dev_newuser(self, ctx):
        member = ctx.message.author
        server = self.bot.get_server('226084200405663754')
        notices = server.get_channel('246162218104782848')
        tedit = await self.bot.get_message(notices, '321717608699265024')
        await self.totmem()
        toch = "Total member count is: " + str(self.v.totamemb) + "\n" + "Welcome to our newest user, " + str(
            member.mention) + "!"
        file = open('../memcount.txt', 'w')
        file.write(str(self.v.totamemb))
        file.close()
        await self.bot.edit_message(tedit, toch)
        role = discord.utils.get(member.server.roles, name = '@updaters')
        await self.bot.add_roles(member, role)

    @bot.command(pass_context = True)
    @permcheck(owners = ['tgwaf'])
    async def dev_swapsies(self, ctx):
        print("got a swapsie request")
        role = discord.utils.get(ctx.message.server.roles, name = '@updaters')
        for member in self.bot.get_server('226084200405663754').members:
            print("Handling the member..." + str(member.name))
            if role in member.roles:
                await self.bot.remove_roles(ctx.message.author, role)
                print("removing updater")
            else:
                await self.bot.add_roles(ctx.message.author, role)
                print("Adding it!")
        tmp = await self.bot.say('Done?')
        await asyncio.sleep(30)
        await self.bot.delete_message(tmp)
        await self.bot.delete_message(ctx.message)

    @bot.command(pass_context = True)
    async def say(self, ctx, *, tosay):
        await self.bot.delete_message(ctx.message)
        if ctx.message.author.id in [self.owners[x] for x in ['klok', 'tgwaf']]:
            tmp = await self.bot.say(tosay)
            await asyncio.sleep(60)
            await self.bot.delete_message(tmp)

    @bot.command(pass_context = True)
    @permcheck(owners = ['tgwaf', 'fawful'])
    async def avatar(self, ctx):
        if ctx.message.attachments:
            thing = ctx.message.attachments[0]['url']
        else:
            url = ctx.message.content[4:]
            thing = url.strip('<>')
        async with self.bot.session.get(thing) as res:
            await self.bot.edit_profile(avatar = await res.read())
        tmp = await self.bot.say("Done it for you, master " + str(ctx.message.author.mention))
        await asyncio.sleep(30)
        await self.bot.delete_message(tmp)

    @bot.command(pass_context = True)
    async def newpart(self, ctx):
        print("Message author: " + str(ctx.message.author) + " Says: " + str(ctx.message.content))
        if ctx.message.server == self.bot.get_server('226084200405663754'):
            readit = []
            file = open('../donediscord.txt', 'r')
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
            post = await self.r.get_submission(submission_id = subid)
            text = str(post.selftext)
            uwc = []
            wc = 0
            for i in str(post.selftext).split():
                if i not in uwc:
                    wc += 1
                    uwc.append(i)
            fulltosay = str(post.title) + "\n" + str(
                post.permalink) + "\n" + "Wordcount of this part was: " + str(
                len(str(post.selftext).split())) + ", the character count was: " + str(
                len(str(text))) + " and the unique word count was: " + str(wc)
            tmp = await self.bot.say(fulltosay)
            await asyncio.sleep(120)
            await self.bot.delete_message(tmp)
            await self.bot.delete_message(ctx.message)
        else:
            readit = []
            file = open('../donediscord.txt', 'r')
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
            post = await self.r.get_submission(submission_id = subid)
            text = str(post.selftext)
            await self.bot.say(str(post.title))
            append = "\n" + "Wordcount of this part was: " + str(
                len(str(post.selftext).split())) + ", the character count was: " + str(
                len(str(post.selftext))) + " and the unique word count was: " + str(
                await uwordcount(post.selftext))
            self.bot.loop.create_task(self.bot.discordify(text, ctx.message.channel, append))

    @bot.command(pass_context = True)
    async def part(self, ctx):
        found = False
        print("Message author: " + str(ctx.message.author) + " Says: " + str(ctx.message.content))
        number = str(ctx.message.content).split()[1]
        query = "Part " + number
        if ctx.message.server == self.bot.get_server('226084200405663754'):
            for submission in await self.r.search(str(query), subreddit = 'thecryopodtohell'):
                if not found:
                    author = submission.author
                    title = str(submission.title)
                    if str(author).lower() == "klokinator" and title.startswith(query):
                        post = submission
                        text = str(post.selftext)
                        uwc = []
                        wc = 0
                        for i in str(post.selftext).split():
                            if i not in uwc:
                                wc += 1
                                uwc.append(i)
                        fulltosay = str(post.title) + "\n" + str(
                            post.permalink) + "\n" + "Wordcount of this part was: " + str(
                            len(str(post.selftext).split())) + ", the character count was: " + str(
                            len(str(text))) + " and the unique word count was: " + str(wc)
                        tmp = await self.bot.say(fulltosay)
                        await asyncio.sleep(120)
                        await self.bot.delete_message(tmp)
                        await self.bot.delete_message(ctx.message)
                        found = True
        else:
            for submission in await self.r.search(str(query), subreddit = 'thecryopodtohell'):
                if not found:
                    author = submission.author
                    title = str(submission.title)
                    if str(author).lower() == "klokinator" and title.startswith(query):
                        post = submission
                        text = str(post.selftext)
                        await self.bot.say(str(post.title))
                        append = "\n" + "Wordcount of this part was: " + str(
                            len(str(post.selftext).split())) + ", the character count was: " + str(
                            len(str(post.selftext))) + " and the unique word count was: " + str(
                            await uwordcount(post.selftext))
                        self.bot.loop.create_task(self.discordify(text, ctx.message.channel, append))
                        found = True

    @bot.command(pass_context = True)
    async def stats(self, ctx):
        self.v.ehashappened = False
        if not self.v.enabled == 0:
            if ctx.message.server != self.bot.get_server('226084200405663754'):
                tmp = await self.bot.say("Starting statter now! Processed: " + str(self.v.totproc))
                while self.v.finished == 0:
                    await self.bot.edit_message(tmp, "Starting statter now! Processed: " + str(self.v.totproc))
                    await asyncio.sleep(0.25)
                self.bot.loop.create_task(self.discordify(self.v.stat, ctx.message.channel, self.v.append,
                                                          deletemess = True, deletetime = 600, character_limit = 1900))
            return

        self.v.enabled = 1
        self.v.finished = 0

        if (ctx.message.author.id not in [self.owners[x] for x in ['tgwaf', 'klok']]) and \
                (ctx.message.server != self.bot.get_server('226084200405663754')):
            print(str(ctx.message.content))

            self.v.stat = ""
            self.v.totups = 0
            self.v.totproc = 0
            self.v.totwc = 0
            self.v.totuwc = 0
            self.v.totcc = 0
            self.v.biggestpart = 0
            self.v.biggesttitle = ""

            tmp = await self.bot.say("Starting statter now! Processed: 0")
            for submission in await self.r.get_new(limit = 750):
                author = submission.author
                title = str(submission.title)
                if title.startswith('Part') and str(author).lower() == "klokinator":
                    wordcount = str(len(str(submission.selftext).split()))
                    charcount = str(len(str(submission.selftext)))
                    unwordcount = str(await uwordcount(submission.selftext))
                    self.v.stat = ("{}: Upvotes: {}, Wordcount: {}, Character Count: {}, "
                                   "Unique Wordcount: {}\n{}").format(title, str(submission.ups), wordcount,
                                                                      charcount, unwordcount, self.v.stat)

                    self.v.totups += int(submission.ups)
                    self.v.totproc += 1
                    self.v.totwc += int(wordcount)
                    self.v.totuwc += int(unwordcount)
                    self.v.totcc += int(charcount)
                    if int(charcount) > self.v.biggestpart:
                        self.v.biggestpart = int(charcount)
                        self.v.biggesttitle = title
                    print(str(self.v.totproc))
                    await self.bot.edit_message(tmp, "Starting statter now! Processed: " + str(
                        self.v.totproc) + ", current CPU usage: " + str(psutil.cpu_percent(interval = None)) + "%")
                    await asyncio.sleep(0.25)

            self.v.append = ("\nTotal upvotes: {}, total submissions processed: {}, "
                             "average upvotes per submission: {}, "
                             "total wordcount: {}, total character count: {}, total unique wordcount: {}, "
                             "average wordcount: {}, average character count: {}, "
                             "average unique wordcount (per-post): {}, "
                             "largest part: {} kloking in at over {} characters!").format(
                str(self.v.totups),
                str(self.v.totproc),
                str(round(float(self.v.totups / self.v.totproc), 2)),
                str(self.v.totwc),
                str(self.v.totcc),
                str(self.v.totuwc),
                str(round(float(self.v.totwc / self.v.totproc), 2)),
                str(round(float(self.v.totcc / self.v.totproc), 2)),
                str(round(float(self.v.totuwc / self.v.totproc), 2)),
                str(self.v.biggesttitle),
                str(self.v.biggestpart))

            self.bot.loop.create_task(self.discordify(self.v.stat, ctx.message.channel, self.v.append,
                                                      deletemess = True, deletetime = 600, character_limit = 1900))
            self.v.finished = 1
            self.v.enabled = 0
            return

        elif (ctx.message.author.id not in [self.owners[x] for x in ['tgwaf', 'klok']]) and \
                (ctx.message.server == self.bot.get_server('226084200405663754')):
            tmp = await self.bot.say("Not in this channel, " + str(ctx.message.author.mention) + "!")
            await asyncio.sleep(30)
            await self.bot.delete_message(tmp)
            return

        print(str(ctx.message.content))
        self.v.stat = ""
        self.v.totups = 0
        self.v.totproc = 0
        self.v.totwc = 0
        self.v.totuwc = 0
        self.v.totcc = 0
        self.v.biggestpart = 0
        self.v.biggesttitle = ""

        total_global_uwc = []
        global_uwc_count = 0

        tmp = await self.bot.say("Starting statter now! Processed: 0")
        for submission in await self.r.get_new(limit = 750):
            author = submission.author
            title = str(submission.title)
            if re.match(r"Part [0-9]+.*", title) and str(author).lower() == "klokinator":
                try:
                    wordcount = str(len(str(submission.selftext).split()))
                    charcount = str(len(str(submission.selftext)))
                    pp_uwc = []
                    pp_wc = 0
                    for i in str(submission.selftext).split():
                        for ind_word in i.lower().split("-"):
                            if ind_word.endswith("'s"):
                                ind_word = ind_word[:-2]
                            punctuation_table = str.maketrans({key: None for key in string.punctuation})
                            ind_word = ind_word.translate(punctuation_table)
                            if ind_word not in pp_uwc:
                                pp_wc += 1
                                pp_uwc.append(ind_word)
                            if ind_word not in total_global_uwc:
                                total_global_uwc.append(ind_word)
                    unwordcount = str(await uwordcount(submission.selftext))
                    self.v.stat = title + ": Upvotes: " + str(submission.ups) + ", Wordcount: " + str(
                        wordcount) + ", Character Count: " + str(
                        charcount) + ", Unique Wordcount: " + str(unwordcount) + "\n" + str(self.v.stat)
                    self.v.totups += int(submission.ups)
                    self.v.totproc += 1
                    self.v.totwc += int(wordcount)
                    self.v.totuwc += int(unwordcount)
                    self.v.totcc += int(charcount)
                    if int(charcount) > self.v.biggestpart:
                        self.v.biggestpart = int(charcount)
                        self.v.biggesttitle = title
                    print(str(self.v.totproc))
                    if self.v.totproc % 25 == 0:

                        await self.bot.edit_message(tmp, ("Starting statter now!"
                                                          " Processed: {}, current CPU usage: {}%").format(
                            str(self.v.totproc),
                            str(psutil.cpu_percent(interval = None))))

                        await asyncio.sleep(0.25)

                except Exception as e:
                    print(str(e))
                    if not self.v.ehashappened:
                        self.v.tosenderr = "Error has occurred! Beginning error message!" + "\n" + "\n" \
                                           + "```" + title + " : " + str(e) + "```"
                        self.v.errmsg = await self.bot.say(self.v.tosenderr)
                        self.v.ehashappened = True
                    else:
                        lento = len(self.v.tosenderr)
                        newlen = lento - 4
                        self.v.tosenderr = self.v.tosenderr[:newlen] + "\n" + title + " : " + e + "```"
                        await self.bot.edit_message(self.v.errmsg, self.v.tosenderr)
        for _ in total_global_uwc:
            global_uwc_count += 1

        self.v.append = ("\nTotal upvotes: {}, total submissions processed: {}, "
                         "average upvotes per submission: {}, "
                         "total wordcount: {}, total character count: {}, total unique wordcount: {}, "
                         "average wordcount: {}, average character count: {}, "
                         "average unique wordcount (per-post): {}, "
                         "largest part: {} kloking in at over {} characters!").format(
            str(self.v.totups),
            str(self.v.totproc),
            str(round(float(self.v.totups / self.v.totproc), 2)),
            str(self.v.totwc),
            str(self.v.totcc),
            str(self.v.totuwc),
            str(round(float(self.v.totwc / self.v.totproc), 2)),
            str(round(float(self.v.totcc / self.v.totproc), 2)),
            str(round(float(self.v.totuwc / self.v.totproc), 2)),
            str(self.v.biggesttitle),
            str(self.v.biggestpart))

        self.bot.loop.create_task(
            self.discordify(self.v.stat, ctx.message.channel, self.v.append, deletemess = True, deletetime = 600,
                            character_limit = 1900, delay = True))
        self.v.finished = 1
        self.v.enabled = 0
        await asyncio.sleep(30)
        await self.bot.delete_message(tmp)

    @bot.command(pass_context = True)
    async def cancel(self, ctx):
        if ctx.message.author.id in [self.owners[x] for x in ['tgwaf', 'klok']]:
            tmp = await self.bot.say("ATTEMPTING TO CANCEL ALL RUNNING TASKS!")
            try:
                await self.bot.edit_message(tmp, ("CANCELLED ALL OTHER RUNNING TASKS. CANCELLING MYSELF NOW. IF THERE "
                                                  "IS NO RESPONSE FROM HERE, ASSUME I CANCELLED MYSELF SUCCESSFULLY."))
                os._exit(1)
            except Exception as e:
                await self.bot.edit_message(tmp, "Sorry, boss... I failed. Here's my exception...: " + str(e))
        else:
            tmp = await self.bot.say("Pfft, no.")
            await asyncio.sleep(30)
            await self.bot.delete_message(tmp)

    @bot.command()
    @permcheck(check = ['tgwaf'])
    async def colour(self):
        brole = discord.utils.get(self.bot.get_server('226084200405663754').roles, name = 'Bot')
        bcol = brole.colour
        erole = discord.utils.get(self.bot.get_server('226084200405663754').roles, name = '@everyone')
        ecol = erole.colour
        curole = discord.utils.get(self.bot.get_server('226084200405663754').roles, name = 'Bot Dev')
        cucol = curole.colour
        if cucol == bcol:
            await self.bot.edit_role(self.bot.get_server('226084200405663754'), curole, colour = ecol)
        else:
            await self.bot.edit_role(self.bot.get_server('226084200405663754'), curole, colour = bcol)

    @bot.command(pass_context = True)
    async def reboot(self, ctx):
        if ctx.message.author in [self.owners[x] for x in ['tgwaf', 'klok']]:
            tmp = await self.bot.say("Restarting!")
            os.system('shutdown -r -t now now')
            await asyncio.sleep(5)
            await self.bot.edit_message(tmp, "Reboot failed!")
        else:
            tmp = await self.bot.say("Heh... No perms, I see? Not happening :)")
            await asyncio.sleep(20)
            await self.bot.delete_message(tmp)
            await self.bot.delete_message(ctx.message)

    @bot.command(pass_context = True)
    @permcheck(check = 'dm_only')
    async def allparts(self, ctx):
        self.v.aptosend = ""
        if self.v.apenabled == 0:
            self.v.apenabled = 1
            self.v.apfinished = 0
            self.v.aptotproc = 0
            if ctx.message.server != self.bot.get_server('226084200405663754'):
                tmp = await self.bot.say("Starting partfinder now! Processed: 0")
                for submission in await self.r.get_new(limit = 750):
                    author = submission.author
                    title = str(submission.title)
                    if title.startswith('Part') and str(author).lower() == "klokinator":
                        self.v.aptosend = ("~~" + " " * 232 + "~~" + title +
                                           "\n" + str(submission.selftext) + "\n" + "\n" + self.v.aptosend)

                        self.v.aptotproc += 1
                    await self.bot.edit_message(tmp, "Starting partfinder now! Processed: " + str(
                        self.v.aptotproc) + ", current CPU usage: " + str(psutil.cpu_percent(interval = None)) + "%")
                    await asyncio.sleep(0.5)
                self.v.apappend = "\n" + "\n" + "That took me a long time. You should be grateful."
                self.bot.loop.create_task(self.discordify(self.v.aptosend, ctx.message.channel, self.v.apappend))
                self.v.apfinished = 1
                self.v.apenabled = 0
        else:
            if ctx.message.server != self.bot.get_server('226084200405663754'):
                tmp = await self.bot.say("Starting partfinder now! Processed: " + str(
                    self.v.aptotproc) + ", current CPU usage: " + str(psutil.cpu_percent(interval = None)) + "%")
                while self.v.apfinished == 0:
                    await self.bot.edit_message(tmp, "Starting partfinder now! Processed: " + str(self.v.aptotproc))
                    await asyncio.sleep(0.25)
                self.bot.loop.create_task(self.discordify(self.v.aptosend, ctx.message.channel, self.v.apappend))

    @bot.command()
    @permcheck(owners = ['tgwaf', 'klok'])
    async def selfclean(self):
        self.bot.loop.create_task(self.self_cleaner())

    @bot.command(pass_context = True)
    @permcheck(owners = ['tgwaf', 'klok'])
    async def ev(self, ctx, *, code):
        await self.bot.delete_message(ctx.message)
        exec(code)

    # ===============
    # task methods
    # ===============
    async def new_part_checker(self):
        while True:
            try:
                fixit = []
                for submission in await self.r.get_new(limit = 3):
                    author = submission.author
                    title = str(submission.title)
                    id_ = str(submission.id)
                    file = open('../donediscord.txt', 'r+')
                    for line in file:
                        linelen = len(line)
                        newlinelen = linelen - 1
                        if line[:newlinelen] not in fixit:
                            fixit.append(line[:newlinelen])
                    if str(author).lower() == "klokinator" and title.lower().startswith('part') and id_ not in fixit:
                        # or str(author).lower() == "thomas1672" and title[0:4].lower() == "test" and id_ not in fixit:
                        file.write(id_ + "\n")
                        file.close()
                        uwc = []
                        wc = 0
                        for i in str(submission.selftext).split():
                            if i not in uwc:
                                wc += 1
                                uwc.append(i)
                        topost = "@everyone - " + title + " - <" + submission.permalink + ">" + \
                                 " Wordcount of this part: " + str(len(str(submission.selftext).split())) + \
                                 ", character count: " + str(len(str(submission.selftext))) + \
                                 " unique word count: " + str(wc)
                        await self.bot.send_message(self.bot.get_channel('226088087996989450'), topost)
                    else:
                        file.close()
                await asyncio.sleep(15)
            except Exception as e:
                print(str(e))

    async def game_updater(self):
        while True:
            await self.bot.change_presence(
                game = discord.Game(name = str(psutil.cpu_percent(interval = None)) + "% CPU Usage!"))
            await asyncio.sleep(2)

    async def self_cleaner(self):
        while True:
            counter = 0
            channels = ['229813048905302017', '226084200405663754']
            for i in channels:
                async for log in self.bot.logs_from(self.bot.get_channel(i), limit = 500):
                    if log.author == self.bot.user:
                        await self.bot.delete_message(log)
                        print("Deleting a message!")
                        counter += 1
                    elif log.content.startswith('!'):
                        await self.bot.delete_message(log)
                        counter += 1
            print("Done cleaning, " + "! I cleaned up " + str(counter) + " messages!")
            await asyncio.sleep(2000)

    async def totmem(self):
        if not self.v.addedu:
            self.v.totamemb = 0
            for _ in self.bot.get_server('226084200405663754').members:
                self.v.totamemb += 1
            self.v.addedu = True
            print("Total members calculated! Total is: " + str(self.v.totamemb))

    async def delete_this_message(self, mess, whento = 0):
        await asyncio.sleep(whento)
        await self.bot.delete_message(mess)

    # ===============
    # helper methods
    # ===============
    async def discordify(self, fullmessage, mesc, append = "", character_limit = 2000, deletemess = False,
                         deletetime = 0, delay = False):
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
            tmp = await self.bot.send_message(mesc, i)
            if deletemess:
                self.bot.loop.create_task(self.delete_this_message(tmp, deletetime))
            if delay:
                await asyncio.sleep(2)


if __name__ == '__main__':
    cryopod = CryopodBot()

    # ===============
    # bot events
    # ===============
    @cryopod.bot.event
    async def on_ready():
        print('LOGGED IN!')
        cryopod.bot.loop.create_task(cryopod.new_part_checker())
        cryopod.bot.loop.create_task(cryopod.game_updater())
        cryopod.bot.loop.create_task(cryopod.self_cleaner())
        cryopod.bot.loop.create_task(cryopod.totmem())

    @cryopod.bot.event
    async def on_member_join(member):
        server = cryopod.bot.get_server('226084200405663754')
        notices = server.get_channel('246162218104782848')
        tedit = await cryopod.bot.get_message(notices, '321717608699265024')
        await cryopod.totmem()
        toch = "Total member count is: " + str(cryopod.v.totamemb) + "\n" + "Welcome to our newest user, " + str(
            member.mention) + "!"

        with open('../memcount.txt', 'w') as file:
            file.write(str(cryopod.v.totamemb))

        await cryopod.bot.edit_message(tedit, toch)
        role = discord.utils.get(member.server.roles, name = '@updaters')
        await cryopod.bot.add_roles(member, role)

    cryopod.bot.run(DISCORD_TOKEN)
