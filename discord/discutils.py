from threading import Thread
import asyncio
import praw
import prawcore
import time
from discord.ext import commands

owners = {
    'klok': '163936232559083520',
    'tgwaf': '230778630597246983',
    'fawful': '135514635129323520',
    'ala': '164200221746790400',
    'tritium': '253942046451171328'
}


class RThreadWrapper:
    def __init__(self):
        useragent = "CryoChecker 1.0"
        self.r = praw.Reddit('CryoChecker', user_agent = useragent)

        self.subreddit = self.r.subreddit("thecryopodtohell")

    async def generic_get(self, job, **kwargs):

        thrd = RThread(job, self, subreddit = self.subreddit, **kwargs)
        thrd.start()

        while not thrd.done:
            await asyncio.sleep(0.5)

        return thrd.returnls

    async def new(self, limit = 0):
        return await self.generic_get('new', limit = limit)

    async def submission(self, id_):
        subls = await self.generic_get('submission', subid = id_)
        return subls[0]

    async def search(self, query):
        return await self.generic_get('search', query = query)


class RThread(Thread):
    def __init__(self, job, wrapper, **kwargs):

        # the job needed to be done.
        self.job = job
        self.r = wrapper.r
        self.subreddit = wrapper.subreddit

        self.limit = kwargs.get('limit', 0)
        self.subid = kwargs.get('subid', '')
        self.query = kwargs.get('query', '')
        self.subreddit = kwargs.get('subreddit', '')

        self.done = False
        self.returnls = []

        super(RThread, self).__init__()

    def run(self):
        job = getattr(self, self.job)

        if callable(job):
            while not self.done:
                try:

                    templs = job()
                    self.returnls.extend(templs)
                    self.done = True

                except prawcore.PrawcoreException:
                    time.sleep(10)

    def new(self):
        templs = []

        for submission in self.subreddit.new(limit = self.limit):
            templs.append(submission)

        return templs

    def submission(self):
        submission = self.r.submission(id = self.subid)
        submission._fetch()

        return [submission]

    def search(self):
        templs = []

        for submission in self.subreddit.search(self.query):
            templs.append(submission)

        return templs


class Vars:
    def __init__(self):
        self.enabled = 0
        self.apenabled = 0
        self.totamemb = 0
        self.totups = 0
        self.totproc = 0
        self.totwc = 0
        self.totuwc = 0
        self.totcc = 0
        self.biggestpart = 0
        self.aptotproc = 0
        self.finished = 0
        self.stat = ''
        self.biggesttitle = ''
        self.append = ''
        self.tosenderr = ''
        self.aptosend = ''
        self.apappend = ''
        self.apfinished = ''
        self.addedu = False
        self.ehashappened = False
        self.errmsg = None


async def uwordcount(text):
    uwc = []
    wc = 0
    for i in str(text).split():
        if i not in uwc:
            wc += 1
            uwc.append(i)
    return wc


def permcheck(**kwargs):
    def predicate(ctx):
        owners_ = kwargs.get('owners', [])
        check = kwargs.get('check', '')

        if type(owners_) is not list:
            owners_ = [owners_]

        if ctx.message.author.id in [owners[x] for x in owners_]:
            return True

        if check == 'dm_only' and ctx.message.server is None:
            return True

        return False

    return commands.check(predicate)
