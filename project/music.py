import discord
from discord.ext import commands
import youtube_dl


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

        ctx.voice_client.stop()

        YDL_OPTIONS = {'format': "bestaudio"}
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                          'options': '-vn'}
        vc = ctx.voice_client

        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
            url2 = info['formats'][0]['url']
            source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
            vc.play(source)

    @commands.command(name='fila')
    async def queue(self, ctx):
        retval = ''
        music_queue = []

        for i in range(0, len(music_queue)):
            if i > 4: break
            retval += music_queue[i][0]['titulo'] + '\n'

        if retval != "":
            await ctx.send(retval)
        else:
            await ctx.send('sem música na lista')

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