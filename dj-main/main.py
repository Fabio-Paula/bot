import discord
from discord.ext import commands
import music
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

    

client.run("OTMxOTcxNzU3NTU0OTQ2MDc4.GOIsTB.58JNo2IuMzBbF3v6BBqzG6N96NSknvX9NJSKbs")
