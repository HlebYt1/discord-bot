import os
import psycopg2
import discord
from discord.ext import commands
import re

class database:
    def __init__(self, client):
        self.client = client
        self.conn = None

    @commands.command(pass_context=True)
    async def scan(self, ctx):
        self.conn = await self.load()
        self.cur = self.conn.cursor()
        for member in ctx.message.server.members:
            self.cur.execute("""UPDATE users SET u_name=E'{name}' WHERE user_id={userID}""".format(userID = member.id, name = re.escape(member.name)))
            self.conn.commit()
        print("Members in {} registered on database".format(ctx.message.server))
        self.cur.close()
        self.conn.close()

    @commands.group(pass_context=True)
    async def db(self, ctx):
        await self.client.send_message(ctx.message.channel ,"database command recieved")
        if ctx.invoked_subcommand is None:
            await self.client.say("incorrect subcommand")
    

    async def load(self):
            return psycopg2.connect(os.environ["DATABASE_URL"], sslmode="require")




def setup(client):
    client.add_cog(database(client))