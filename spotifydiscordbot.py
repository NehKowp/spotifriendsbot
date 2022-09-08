from typing import Optional
import requests
import discord
from discord import app_commands
import random as rand
import io
import PIL.Image as PIL
import json


def statistics(user1,user2):
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
    
def genrestats(user1):
    r = requests.post('https://spotifriends-xfsi2jbksq-ew.a.run.app/name', json={"name": user1,"function": "g"})
    return r.json()


class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)

        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        
        await self.tree.sync()


intents = discord.Intents.default()
client = MyClient(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')


@client.tree.command()
async def helpspotifriends(interaction: discord.Interaction):
    """Help for SpotiFriends Bot!"""
    embed=discord.Embed(title='Help for SpotiFriends Bot',color=0x21c452)
    embed.add_field(name="**__ Statistiques :__**", value="`/stats user1 user2`", inline=False)
    embed.add_field(name="**__ Titres en Communs :__**", value="`/common user1 user2`", inline=False)
    embed.add_field(name="**__ Genres Préférés :__**", value="`/genres user1`", inline=False)

    embed.set_footer(text="*SpotiFriends by Kow_p*")

    await interaction.response.send_message(embed = embed)


@client.tree.command()
@app_commands.describe(
    first_value='The link profile of the first user',
    second_value='The link profile of the second user you want to compare',
)
async def stats(interaction: discord.Interaction, first_value: str, second_value: str):
    """Compare the Spotify's stats of 2 users."""
    await interaction.response.defer()
    data = statistics(first_value,second_value)
    pourcentage = data[0]
    titrecommun = data[1]
    embed=discord.Embed(title='Stats',color=0x21c452)
    embed.add_field(name="**__Titres en Commun :__**", value="`"+str(titrecommun)+"`", inline=False)
    embed.add_field(name="**__Pourcentage :__**", value="`"+str(pourcentage)+" %"+"`", inline=False)
    embed.set_footer(text="*SpotiFriends by Kow_p*")
    await interaction.followup.send(embed = embed)



@client.tree.command()
@app_commands.describe(
    first_value='The link profile of the first user',
    second_value='The link profile of the second user you want to compare',
)
async def common(interaction: discord.Interaction, first_value: str, second_value: str):
    """Show Spotify's songs in common of the 2 users."""
    await interaction.response.defer()
    data = titrecom(first_value,second_value)
    print(data)
    embed2=discord.Embed(title='Song In Commons ',color=0x21c452)
    i=0
    for titre in data:
            embed2.add_field(
                name="**"+str(data[i][0])+"**",
                value="`"+str(data[i][1])+"`",
                inline=True
                )
            i+=1
    embed2.set_image(url=data[rand.randint(0,(len(data)-1))][2])
    await interaction.followup.send(embed = embed2)

@client.tree.command()
@app_commands.describe(
    first_value='The link profile of the user')
async def genres(interaction: discord.Interaction, first_value: str):
    await interaction.response.defer()
    """Show the different musics tastes and genres of the choosen user"""
    resp = genrestats(first_value)
    embed=discord.Embed(title='Genres',color=0x21c452)
    embed.add_field(name="**__Genres préférés de __**", value="`"+first_value+"`", inline=False)
    by = bytes(resp["data"])
    buf = io.BytesIO(by)
    image = PIL.open(buf)
    image.save("./genrestats.png")
    file = discord.File("./genrestats.png", filename="genrestats.png")
    embed.set_image(url="attachment://genrestats.png")
    embed.set_footer(text="*SpotiFriends by Kow_p*")
    await interaction.followup.send(embed = embed, file=file)

with open('./config.json', 'r') as f:
    config = json.load(f)
    dstoken = config['Discord Bot Token']

client.run(dstoken)
