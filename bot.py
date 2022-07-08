import discord
import random
from random import choice
from discord.ext import tasks, commands
import requests

def requestDefinition(word):
  try:
    url = f"""https://api.dictionaryapi.dev/api/v2/entries/en/{word}"""
    content = requests.get(url).json()
    try:
      definition = content[0]
    except:
      definition = None
    return definition
  except:
    return "Invalid input"


client = commands.Bot(command_prefix="?")
status = ["Discord bro, what did you expect?"]

@client.event
async def on_ready():
  apply_status.start()
  print('Logged in as {0.user}'.format(client))

@tasks.loop(seconds=600)
async def apply_status():
  await client.change_presence(activity=discord.Game(choice(status)))

@client.command(name="hello", help="Greets user")
async def hello(ctx):
  username=str(ctx.author).split('#')[0]
  await ctx.send(f'Hello {username}!')

@client.command(name="bye", help="Farewell message")
async def bye(ctx):
  username=str(ctx.author).split('#')[0]
  await ctx.send(f'Bye {username}!')

@client.command(name="saytheline", help="Displays the iconic quote")
async def saytheline(ctx):
  await ctx.send(f'insert your quote')

@client.command(name="pp", help="shows pp size")
async def pp(ctx):
  username=str(ctx.author).split('#')[0]
  size = random.randint(0,50)
  pp_format = '8'
  for i in range(size):
    pp_format+='='
  pp_format+='D'
  await ctx.send(f'{pp_format}')  
  await ctx.send(f"{username}'s pp size is {size} inches")  
  
@client.command(name="pfp", help="shows pfp")
async def pfp(ctx):
  username=str(ctx.author).split('#')[0]
  # userID = str(ctx.author.id)
  # user = get(client.get_all_members(), id=userID)
  user = ctx.author
  pfp = user.avatar_url
  embed=discord.Embed(title="test", description='{},test'.format(user.mention) , color=0xecce8b)
  embed.set_image(url=(pfp))
  await ctx.send(username, embed=embed)

####################################################################################
@client.command(name="define", help="shows finds definition of the word")
async def define(ctx):
  await ctx.trigger_typing()
  username=str(ctx.author).split('#')[0]
  # userID = str(ctx.author.id)
  # user = get(client.get_all_members(), id=userID)
  user = ctx.author
  word = ctx.message.content.split(" ")[1] 
  definitionContent = requestDefinition(word)
  embed=discord.Embed(title=f"Definition of '{word.lower()}':", description="" , color=discord.Color.purple())
  embed.set_author(name=f"Big Brain Dictionary", url="", icon_url=f"{client.user.avatar_url}")
  embed.set_thumbnail(url="")
  if definitionContent == None:
    await ctx.send("word not found :(")
    return
  if "phonetic" in definitionContent:
    embed.add_field(name=f"phonetic", value=f"{definitionContent['phonetic']}", inline=False)
  else:
    None
  tempDictList = definitionContent['meanings']
  for i in range(len(tempDictList)):
      pos = tempDictList[i]['partOfSpeech']
      defi = tempDictList[i]['definitions'][0]['definition']
      try:
        example = tempDictList[i]['definitions'][0]['example']
      except:
        example = "None"
      try:
        synonyms = ", ".join(tempDictList[i]['definitions'][0]['synonyms'])
      except:
        synonyms = "None"
      try:
        antonyms = ", ".join(tempDictList[i]['definitions'][0]['antonyms'])
      except:
        antonyms = "None" 
      embed.add_field(name=f"{pos}", value=f"{defi}", inline=False)
      embed.add_field(name=f"example", value=f"{example}", inline=False)
      if synonyms:
        embed.add_field(name=f"synonyms", value=f"{synonyms}", inline=False)
      if antonyms:
        embed.add_field(name=f"antonyms", value=f"{antonyms}", inline=False)
  embed.set_footer(text="requested by: {}".format(ctx.author.display_name))
  await ctx.send(username, embed=embed) 

####################################################################################

@client.command(name="join", help="join voice channel")
async def join(ctx):
  if ctx.author.voice:
    channel = ctx.message.author.voice.channel
    await channel.connect()
  else:
    await ctx.send("please join a voice channel")

@client.command(name="leave", help="leave voice channel")
async def leave(ctx):
  if ctx.voice_client:
    await ctx.guild.voice_client.disconnect()
    await ctx.send("left voice channel")
  else:
    await ctx.send("not in a voice channel")
    

TOKEN = "INSERT TOKEN HERE"
client.run(TOKEN)


