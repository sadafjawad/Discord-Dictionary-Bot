import discord

TOKEN = 'insert token here' 

client = discord.Client()

@client.event
async def on_ready():
  print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  
  username = str(message.author).split('#')[0]
  user_message = str(message.content)

 
  if message.author == client.user:
    return


  if user_message.lower() == 'hello':
    await message.channel.send(f'Hello {username}!')
        
  elif user_message.lower() == 'bye':
    await message.channel.send(f'Bye {username}!')

  elif user_message.lower() == 'saytheline':
    await message.channel.send(f'"Dreams are not what you see in your sleep, dreams are things that do not let you sleep."')

  
client.run(TOKEN)


