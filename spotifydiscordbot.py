import json
import requests
import discord
from discord.ext import tasks
import random as rand
from collections import Counter
import io
import PIL.Image as PIL


def stats(user1,user2):
    r = requests.post('https://spotifriends-xfsi2jbksq-ew.a.run.app/name', json={
  "name": [user1,user2],
  "function": "s"
}
)
    return r.json()['data']
def titrecom(user1,user2):
    r = requests.post('https://spotifriends-xfsi2jbksq-ew.a.run.app/name', json={
  "name": [user1,user2],
  "function": "c"
}
)
    return r.json()['data']
    
def genres(user1):
    r = requests.post('https://spotifriends-xfsi2jbksq-ew.a.run.app/name', json={"name": user1,"function": "g"})
    return r.json()


dsclient = discord.Client()
with open('./config.json', 'r') as f:
    config = json.load(f)
    dstoken = config['Discord Bot Token']
    dschannel = int(config['Discord Channel ID'])

@dsclient.event
async def on_ready():
    print('We have logged in as {0.user}'.format(dsclient))
    channel = dsclient.get_channel(dschannel)
    await channel.send("`"+"Connecté"+"`")

@dsclient.event
async def on_message(message):
    if message.author == dsclient.user:
        return

    if message.content.startswith('!spotistats'):
        msg = message.content
        listpseudo=msg.split()
        user1=listpseudo[1] 
        user2=listpseudo[2]

        data = stats(user1,user2)
        pourcentage = data[0]
        titrecommun = data[1]

        embed=discord.Embed(color=0x21c452)
        embed.add_field(name="**__Titres en Commun :__**", value="`"+str(titrecommun)+"`", inline=False)
        embed.add_field(name="**__Pourcentage :__**", value="`"+str(pourcentage)+" %"+"`", inline=False)
        embed.set_footer(text="*SpotiFriends by Kow_p*")
        await message.channel.send(embed=embed)  

    if message.content.startswith('!titrecommuns'):
        msg = message.content
        listpseudo=msg.split()
        user1=listpseudo[1] 
        user2=listpseudo[2]
        data = titrecom(user1,user2)
        embed2=discord.Embed(color=0x21c452)
        i=0
        for titre in data:
                embed2.add_field(
                    name="**"+str(data[i][0])+"**",
                    value="`"+str(data[i][1])+"`",
                    inline=True
                    )
                i+=1
        embed2.set_image(url=data[rand.randint(0,(len(data)-1))][2])
        await message.channel.send(embed=embed2) 

    if message.content.startswith('!genrestats'):
        msg = message.content
        listpseudo=msg.split()
        user1=listpseudo[1] 

        await message.channel.send("`Chargement ...`") 
        resp = genres(user1)

        embed=discord.Embed(color=0x21c452)
        embed.add_field(name="**__Genres préférés de __**", value="`"+user1+"`", inline=False)
        by = bytes(resp["data"])
        buf = io.BytesIO(by)
        image = PIL.open(buf)
        image.save("./genrestats.png")
        file = discord.File("./genrestats.png", filename="genrestats.png")
        embed.set_image(url="attachment://genrestats.png")
        embed.set_footer(text="*SpotiFriends by Kow_p*")
        await message.channel.send(embed=embed, file = file)  
    
    if message.content.startswith('!helpspotifriends'):
        embed=discord.Embed(color=0x21c452)
        embed.add_field(name="**__ Statistiques :__**", value="`!spotistats user1 user2`", inline=False)
        embed.add_field(name="**__ Titres en Communs :__**", value="`!titrecommuns user1 user2`", inline=False)
        embed.add_field(name="**__ Genres Préférés :__**", value="`!genrestats user1`", inline=False)

        embed.set_footer(text="*SpotiFriends by Kow_p*")
        await message.channel.send(embed=embed)  

dsclient.run(dstoken)

