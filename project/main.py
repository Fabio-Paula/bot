import discord
from discord.ext import commands
import youtube_dl
import random

cogs = [music]

client = commands.Bot(command_prefix='.', intents=discord.Intents.all())
bot = client.command('.')

for i in range(len(cogs)):
    cogs[i].setup(client)

@client.command()
async def comandos(ctx):
    await ctx.send('''
```
Comandos
.play (link da música) - tocar uma música
.pause - pausar a música
.resume - continuar a música
.sair - retirar o bot do canal de voz
.ola - cumprimentar o DJPormade
.depende - depende
.calcular (valores) - para fazer calculos
.dado (quantidade) - para ser sorteado um número até um valor estipulado
.segredo - descubra 🤭
```
''')

@client.command(name = 'segredo')
async def secret(ctx):
    try:
        await ctx.author.send('bejo na bunda lindo(a)')
    except discord.errors.Forbidden:
        await ctx.send('Não consigo te contar o segredo, habilite suas mensagens privadas!!')
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if 'depende' in message.content:
        await message.channel.send(f'{message.author.name} Essa palavra está proibída!!')
        await message.delete()
    await client.process_commands(message)

@client.command(name = 'calcular')
async def calculate_expression(ctx, *expression):
    expression = ''.join(expression)
    response = eval(expression)

    await ctx.send('A resposta é ' + str(response))

@client.command()
async def ola(ctx):
    name = ctx.author.name

    response = 'Olá ' + name + '!!'

    await ctx.send(response)

@client.command(name = 'dado')
async def dado(ctx, numero):
    variavel = random.randint(1, int(numero))
    await ctx.send(f'O número da escolhido foi {variavel}')

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

client.run("OTMxOTcxNzU3NTU0OTQ2MDc4.GOIsTB.58JNo2IuMzBbF3v6BBqzG6N96NSknvX9NJSKbs")
