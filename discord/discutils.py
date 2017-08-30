import asyncio
import praw
import OAuth2Util
from threading import Thread
from discord.ext import commands

owners = {
    'klok': '163936232559083520',
    'tgwaf': '230778630597246983',
    'fawful': '135514635129323520'
}


class RThreadWrapper:
    def __init__(self):
        user_agent = "CryoChecker 1.0"
        self.r = praw.Reddit(user_agent = user_agent)
        oauth = OAuth2Util.OAuth2Util(self.r)
        oauth.refresh(force = True)
        self.subreddit = self.r.get_subreddit("thecryopodtohell")

    async def generic_get(self, job, **kwargs):
        thrd = RThread(job, self, **kwargs)
        thrd.start()

        while not thrd.done:
            await asyncio.sleep(2)

        return thrd.returnls

    async def get_new(self, limit = 0):
        return await self.generic_get('get_new', limit = limit)

    async def get_submission(self, submission_id):
        subls = await self.generic_get('get_submission', subid = submission_id)
        return subls[0]

    async def search(self, query, subreddit):
        return await self.generic_get('search', query = query, subreddit = subreddit)


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
        templs = []

        if self.job == 'get_new':
            for submission in self.subreddit.get_new(limit = self.limit):
                self.returnls.append(submission)
            self.returnls.extend(templs)
            self.done = True

        elif self.job == 'get_submission':
            self.returnls.append(self.r.get_submission(submission_id = self.subid))
            self.done = True

        elif self.job == 'search' and self.query:
            for submission in self.r.search(self.query, subreddit = self.subreddit):
                templs.append(submission)
            self.returnls.extend(templs)
            self.done = True


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


def uwordcount(text):
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

