import aiohttp
import discord
from discord.ext import commands
from discutils import RThreadWrapper, Vars, owners
from pw_bot import *


class CryopodBot(commands.Bot):

    def __init__(self):
        # owner ids
        self.owners = owners

        # praw magical thread magic
        self.r = RThreadWrapper()

        # a class to hold all tg's precious global variables
        self.v = Vars()

        # aiohttp session for magix
        self.session = aiohttp.ClientSession()

        super().__init__(command_prefix = '!', description = 'CryopodBot')

    async def totmem(self):
        if not self.v.addedu:
            self.v.totamemb = 0
            serv = self.get_server('226084200405663754')
            # serv = self.get_server('239143828722941952')
            for _ in serv.members:
                self.v.totamemb += 1
            self.v.addedu = True
            print("Total members calculated! Total is: " + str(self.v.totamemb))


if __name__ == '__main__':
    cryopodbot = CryopodBot()

    # ===============
    # bot events
    # ===============
    @cryopodbot.event
    async def on_ready():
        print('LOGGED IN!')

        cryopodbot.load_extension('cryopodcog')

    @cryopodbot.event
    async def on_member_join(member):
        server = cryopodbot.get_server('226084200405663754')
        notices = server.get_channel('246162218104782848')
        tedit = await cryopodbot.get_message(notices, '321717608699265024')
        await cryopodbot.totmem()
        toch = "Total member count is: " + str(cryopodbot.v.totamemb) + "\n" + "Welcome to our newest user, " + str(
            member.mention) + "!"

        with open('../memcount.txt', 'w') as file:
            file.write(str(cryopodbot.v.totamemb))

        await cryopodbot.edit_message(tedit, toch)
        role = discord.utils.get(member.server.roles, name = '@updaters')
        await cryopodbot.add_roles(member, role)

    cryopodbot.run(DISCORD_TOKEN)
