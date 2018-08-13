import discord
import youtube_dl
from discord.ext import commands
import aiohttp
import os
import asyncio

class voice:
    def __init__(self, client):
        self.client = client
        self.players = {}

    @commands.command(pass_context=True)
    async def join(self, ctx):
        self.channel = ctx.message.author.voice.voice_channel
        await self.client.join_voice_channel(self.channel)

    @commands.command(pass_context=True)
    async def leave(self, ctx):
        self.server = ctx.message.server
        self.voice_client = self.client.voice_client_in(self.server)
        await self.voice_client.disconnect()

#---------------------------------------------YOUTUBE---------------------------------------------------------------------------------
    @commands.command(pass_context=True)
    async def play(self, ctx, url):
        self.server = ctx.message.server
        self.voice_client = self.client.voice_client_in(self.server)
        if self.voice_client == None:
            self.voice_client = await self.client.join_voice_channel(ctx.message.author.voice.voice_channel)    
        self.player = await self.voice_client.create_ytdl_player(url)
        self.players[self.server.id] = self.player
        self.player.start()
    
    @commands.command(pass_context=True)
    async def pause(self, ctx):
        self.players[ctx.message.server.id].pause()

    @commands.command(pass_context=True)
    async def resume(self, ctx):
        self.players[ctx.message.server.id].resume()

    @commands.command(pass_context=True)
    async def stop(self, ctx):
        self.players[ctx.message.server.id].stop()

    @commands.command(pass_context=True)
    async def ytdl(self, ctx, url):
        msg = await self.client.say("Nep is trying her hardest to get your file. https://i.kym-cdn.com/photos/images/original/001/283/141/58e.gif")
        process = await asyncio.create_subprocess_shell("youtube-dl --extract-audio --audio-format mp3 -o output.mp3 {}".format(url), stdout=asyncio.subprocess.PIPE)
        stdout, stderr = await process.communicate()
        if os.path.getsize("output.mp3")/1048576 < 7:
            await self.client.send_file(ctx.message.channel,"output.mp3",content="Tada")
            await self.client.delete_message(msg)
        else:
            session = aiohttp.ClientSession()
            upload = open("output.mp3", "rb")
            files = {'filedata': upload}
            resp = await session.post('https://transfer.sh/', data=files)
            upload.close()
            session.close()
            await self.client.edit_message(msg, await resp.text())
        os.remove("output.mp3")
        msg, process, session, upload, files, resp, stdout, stderr = None, None,None,None,None,None,None,None




def setup(client):
    discord.opus.load_opus("vendor/lib/libopus.so.0")
    if discord.opus.is_loaded():
        print("Opus loaded!")

    client.add_cog(voice(client))