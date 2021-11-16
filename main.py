import discord
from googleapiclient.discovery import build
from discord.ext import commands
from PIL import Image, ImageFont, ImageDraw
import requests
import json
import textwrap
import random
import asyncio
import traceback
import sys
from webserver import keep_alive
from discord import Activity, ActivityType
import cowsay


import os

yt_api_key = 'yeehee'

youtube = build("youtube", 'v3', developerKey=yt_api_key)
description = '''blank'''

intents = discord.Intents.default()
client = commands.Bot(command_prefix='$')
Quoteembed = discord.Embed(
        title="Quotes",
        colour=discord.Color.from_rgb(54, 57, 63),
    )

@client.event
async def on_ready():
    await client.change_presence(activity=Activity(name=f"{len(client.guilds)} servers",type=ActivityType.watching))
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    await client.process_commands(message)
    if 'avian' in message.content.lower():
      await client.process_commands(message)
      await message.add_reaction('🦫')
    elif 'tom' in message.content.lower():
      await client.process_commands(message)
      emojis = [ '🇪', '🇵','🇮','🇨']
      for emoji in emojis:
        await client.process_commands(message)
        await message.add_reaction(emoji)

@client.command()
async def invoke(ctx,*, thing):
  ctx.send(str(cowsay.daemon))
@client.command()
async def quote(ctx,*, quote):
  username = ctx.message.author.name
  
  def write_json(new_data, filename='quotes.json'):
      with open(filename,'r+') as file:
            # First we load existing data into a dict.
          file_data = json.load(file)
          # Join new_data with file_data inside emp_details
          file_data["quotes"].append(new_data)
          # Sets file's current position at offset.
          file.seek(0)
          # convert back to json.
          json.dump(file_data, file, indent = 4)
  
      # python object to be appended
  y = f'{username} : {quote}'
      
  write_json(y)

@client.command()
async def delquote(ctx, index):
    f = open('quotes.json', "r")
    data = json.loads(f.read())
    for indexs,i in enumerate(data['quotes']):
      print(indexs,i)

@client.command()
async def quotes(ctx):
  f = open('quotes.json', "r")
  
  data = json.loads(f.read())
  for index, i in enumerate(data['quotes']):
    Quoteembed.add_field(name = f'[{index}]', value = i, inline = 'False')
  await ctx.send(embed = Quoteembed)
  Quoteembed.clear_fields()
  f.close()

@client.command()
async def crisscross(ctx):
  await ctx.send(file=discord.File('video0.mov'))

@client.command()
async def unotips(ctx):
  tips= [
  'Keep +2 and +4 for emergencies',
  'Keep your score low','Change color often',
  'Use action cards smart',
  'Co-operate with other players',
  'Reducing Cards',
  'Avoid someone from going out',
  'Ime mu munni!',
  'Quickly get rid of matched numbers in your hand.',
  'Try to keep your Wild Card until the very end.',
  'Avoid using the reverse card at the wrong time.',
  'Always change the color when playing a Wild Card +4.',
  'Try to keep at least one +2 card in your hand.',
  'Play higher number cards first.',
  'Note the last card color when players have one card left and do not play it.'
  ]
  await ctx.send(random.choice(tips))

@client.command()
async def unofacts(ctx):
  facts= [
'The game was invented in 1971 by Merle Robbins.',
'Uno was created to help solve an argument about Crazy Eights.',
'Merle invested $8,000 to make 5,000 first edition Uno games.',
'Merle Robbins sold the rights to Uno for more than $50,000.',
'Mattel announced in 2019 that Uno is now available in braille.',
'The game has its own unique deck of 108 cards.',
'Your mother has fat',
'Tom is sexy',
'Tom is the #1 uno player in the world',
'Uno sales are still increasing year over year. ',
'Uno is a great way to teach little kids about number and color recognition.','Playing Uno can help children develop fine motor skills.',
'Modern Uno is available in various themes.']
  await ctx.send(random.choice(facts))

@client.command()
@commands.has_permissions(administrator = True)
async def kick(ctx, member : discord.Member,* , reason='None'):
    await member.send(f'{member.mention}, you have been kicked from {member.guild.name} Reason: {reason}')
    await member.kick(reason=reason)
    await ctx.send('Kicked' + member.mention)
    

@client.command()
@commands.has_permissions(administrator = True)
async def ban(ctx, member : discord.Member, *, reason = None):
  await member.send(f'{member.mention}, you have been banned from {member.guild.name} Reason: {reason}')
  await member.ban(reason = reason)
    


@client.command()
@commands.has_permissions(administrator = True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return

@client.command()
@commands.has_permissions(administrator = True)
async def purge(ctx, amount=10):
    await ctx.channel.purge(limit=amount)

@client.command()
async def uplog(ctx):
  uplog = discord.Embed(
        title="Update log",
        colour=discord.Colour.purple(),
    )
  uplog.add_field(name='Version 0.69', value='Uno', inline='False')
  await ctx.send(embed=uplog)
@client.command()
async def commands(ctx):
    Help = discord.Embed(
        title="Tom's bot commands",
        colour=discord.Color.from_rgb(54, 57, 63),
    )
    Help2 = discord.Embed(
        title="Tom's bot commands",
        colour=discord.Color.from_rgb(54, 57, 63),
    )
    
    Help.add_field(name='$ytinfo (*channel username*)', value="```Get info about a youtube channel **(Username only)**```",
                   inline='True')
    Help.add_field(name='$ping', value='```Shows the current ping```', inline='False')
    Help.add_field(name='$inspire', value='```Sends an inspirational quote```', inline='False')
    Help.add_field(name='$8ball (*question*)', value='```Answers your question```', inline='False')
    Help.add_field(name='$kick (*member*) (*reason*)', value='```Kicks the member```', inline='False')
    Help.add_field(name='$ban (*member*) (*reason*)', value='```Bans the member```', inline='False')
    Help.add_field(name='$unban (*member*)', value='```Unbans the member```', inline='False')
    Help.add_field(name='$gaymeter (*member*)', value='```Shows the % of gay```', inline='False')
    Help.add_field(name='$purge (*value*)', value='```Deletes a number of recent messages```', inline='False')
    Help.add_field(name='$uplog ', value="```Shows what's new with the bot```", inline='False')
    global msg
    msg = await ctx.send(embed=Help)
    await msg.add_reaction('⬅️')
    await msg.add_reaction('➡️') 

@client.event
async def on_reaction_add(reaction, user):
  Help2 = discord.Embed(
        title="Tom's bot commands",
        colour=discord.Color.from_rgb(54, 57, 63),
    )
  Help = discord.Embed(
        title="Tom's bot commands",
        colour=discord.Color.from_rgb(54, 57, 63),
    )
  Help2.add_field(name='$unofacts', value='```Facts about uno!```', inline='False')
  Help2.add_field(name='$unotips', value='```Tips to win your next uno game!```', inline='False')
  Help2.add_field(name='$monkey', value='```Surprise in vc! (Soon)```', inline='False')
  Help2.add_field(name='$fuck @user + (optional argument)', value='```Fucks somebody violently in the ass!```', inline='False')
  Help2.add_field(name='$destroypussy', value='```Destroys 1 pussy!```', inline='False')
  Help2.add_field(name='$qute + the quote', value='```Quote somthing cool!```', inline='False')
  Help2.add_field(name='$quotes', value='```Shows the cool quotes!```', inline='False')

  Help.add_field(name='$ytinfo (*channel username*)', value="```Get info about a youtube channel **(Username only)**```",
                   inline='True')
  Help.add_field(name='$ping', value='```Shows the current ping```', inline='False')
  Help.add_field(name='$inspire', value='```Sends an inspirational quote```', inline='False')
  Help.add_field(name='$8ball (*question*)', value='```Answers your question```', inline='False')
  Help.add_field(name='$kick (*member*) (*reason*)', value='```Kicks the member```', inline='False')
  Help.add_field(name='$ban (*member*) (*reason*)', value='```Bans the member```', inline='False')
  Help.add_field(name='$unban (*member*)', value='```Unbans the member```', inline='False')
  Help.add_field(name='$gaymeter (*member*)', value='```Shows the % of gay```', inline='False')
  Help.add_field(name='$purge (*value*)', value='```Deletes a number of recent messages```', inline='False')
  Help.add_field(name='$uplog ', value="```Shows what's new with the bot```", inline='False')

  global msg


  if not user.bot:
    if reaction.emoji == "➡️":
      await reaction.remove(user)
      await msg.edit(embed =Help2)
    elif reaction.emoji == "⬅️":
      await reaction.remove(user)
      await msg.edit(embed =Help)
    




@client.command()
async def up(ctx):
    await ctx.send('Tommy is awake')

@client.command()
async def inspire(ctx):
    def get_quote():
        response = requests.get("https://zenquotes.io/api/random")
        json_data = json.loads(response.text)
        quote = json_data[0]['q'] + ' -' + json_data[0]['a']
        return (quote)

    title_font = ImageFont.truetype('HandyQuomteRegular-6YLLo.ttf', 150)

    quote = get_quote()
    
    msg = quote

    im = Image.open("background.jpg")
    draw = ImageDraw.Draw(im)
    w, h = 2419,1361
    margin = offset = 200
    for line in textwrap.wrap(msg, width=35):
        draw.text((margin, offset), line, font=title_font)
        offset += title_font.getsize(line)[1]

    im.save("hello.png", "PNG")
    # inspire = discord.Embed(
    #     colour=discord.Colour.purple(),
    # )
    # inspire.set_image(url=im)
    await ctx.send(file=discord.File('hello.png'))

@client.command()
async def gaymeter(ctx,member : discord.Member):
 await ctx.send(f'{member.mention} is {random.randint(0, 100)} % gay')
 
@client.command(pass_context=True)
async def fuck(ctx,member : discord.Member ,*,person = None):
  if person == None:
    await ctx.send(f"{member.mention} got fucked")
  else:
    await ctx.send(f"{member.mention}'s {person} got fucked")
global counter
counter = 0
@client.command()
async def destroypussy(ctx):
  global counter
  counter +=1
  await ctx.send(f'Pussy has been destroyed {counter} times :heart_eyes_cat:')

@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)} ms')

@client.command()
async def ytinfo(ctx,*, usr):
    request = youtube.channels().list(
        part=f'contentDetails , statistics ,snippet',
        forUsername=usr
    )
    response = request.execute()
    print(response)
    for item in response['items']:
        print(item)
        subs = item['statistics']['subscriberCount']
        views = item['statistics']['viewCount']
        vids = item['statistics']['videoCount']
        userId = item['id']
        pfp = item['snippet']['thumbnails']['default']['url']
        disname = item['snippet']['title']
        desc = item['snippet']['localized']['description']
        print(pfp)
    ytinfo = discord.Embed(
        title=disname + "'s Channel info",
        colour=discord.Colour.red(),
    )

    ytinfo.add_field(name='Description', value=desc, inline='True')
    ytinfo.add_field(name='Subscribers', value=subs, inline='True')
    ytinfo.add_field(name='Videos', value=vids, inline='False')
    ytinfo.add_field(name='Views', value=views, inline='True')
    ytinfo.add_field(name='Channel id', value=userId, inline='True')
    ytinfo.set_thumbnail(url=pfp)
    await ctx.send(embed=ytinfo)

@client.command(aliases=['8ball'])
async def _8ball(ctx, *,question):
        responses= [
            'Yes',
            'No',
            'Mabye',
            'Who cares',
            'idk']
        await ctx.send(random.choice(responses))

TOKEN = os.environ.get("DISCORD_BOT_SECRET")

keep_alive()
client.run(TOKEN)