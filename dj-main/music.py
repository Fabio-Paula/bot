from http import client
import discord
from discord import FFmpegPCMAudio
from discord import TextChannel
from discord.utils import get
from discord.ext import commands
from youtube_dl import YoutubeDL


class music(commands.Cog):
    def _init_(self, client):
        self.client = client

    @commands.command()
    async def play(self, ctx, url):

        if ctx.author.voice is None:
            await ctx.send('Você precisa estar em um canal de voz')
        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()
        else:
            await ctx.voice_client.move_to(voice_channel)

        YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
        FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        voice = get(client.voice_clients, guild=ctx.guild)

        if not voice.is_playing():
            with YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(url, download=False)
            URL = info['url']
            voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
            voice.is_playing()
            await ctx.send('Bot está tocando')


    @commands.command()
    async def pause(self, ctx):
        await ctx.voice_client.pause()
        await ctx.send('Música Pausada ⏸')

    @commands.command()
    async def resume(self, ctx):
        await ctx.voice_client.resume()
        await ctx.send('Música Retomada ⏯')

    @commands.command()
    async def sair(self, ctx):
        await ctx.voice_client.disconnect()


def setup(client):
    client.add_cog(music(client))