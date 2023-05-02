import os
import json
import requests
import random
import discord
from discord import app_commands

agents = []
champs = []

def get_agent(): # TODO: Find a way to sort agents by role
    global agents
    if agents == []:
        hard_coded_agents = ['Jett', 'Neon', 'Brimstone', 'Cypher', 'Astra', 'Viper', 'Fade', 'Sova', 'Raze', 'Phoenix', 'Breach', 'Chamber', 'Skye', 'Yoru', 'Killjoy', 'Sage', 'Gekko', 'Harbor', 'Reyna', 'Omen', 'KAY/O']
        if os.environ.get("RiotAPIKey") == None: 
            print("No RiotAPIKey found in environment variables, agents are not 100% sure to be up to date")
            agents = hard_coded_agents
        else:
            api_key = os.environ.get("RiotAPIKey")
            request = requests.get(f"https://eu.api.riotgames.com/val/content/v1/contents?locale=en-US&api_key={api_key}")
            if request.status_code == 200:
                agents = list(set([character["name"] for character in request.json().get("characters") if character["name"] != "Null UI Data!"]))
            else:
                print(f"Error while getting agents from Riot API, status code: {request.status_code}")
                agents = hard_coded_agents
    return agents[random.randint(0, len(agents) - 1)]

def get_champion(): #TODO: Find a way to sort champions by role
    global champs
    if champs == []:
        hard_coded_champs = ['Aatrox', 'Ahri', 'Akali', 'Akshan', 'Alistar', 'Amumu', 'Anivia', 'Annie', 'Aphelios', 'Ashe', 'Aurelion Sol', 'Azir', 'Bard', "Bel'Veth", 'Blitzcrank', 'Brand', 'Braum', 'Caitlyn', 'Camille', 'Cassiopeia', "Cho'Gath", 'Corki', 'Darius', 'Diana', 'Draven', 'Dr. Mundo', 'Ekko', 'Elise', 'Evelynn', 'Ezreal', 'Fiddlesticks', 'Fiora', 'Fizz', 'Galio', 'Gangplank', 'Garen', 'Gnar', 'Gragas', 'Graves', 'Gwen', 'Hecarim', 'Heimerdinger', 'Illaoi', 'Irelia', 'Ivern', 'Janna', 'Jarvan IV', 'Jax', 'Jayce', 'Jhin', 'Jinx', "Kai'Sa", 'Kalista', 'Karma', 'Karthus', 'Kassadin', 'Katarina', 'Kayle', 'Kayn', 'Kennen', "Kha'Zix", 'Kindred', 'Kled', "Kog'Maw", "K'Sante", 'LeBlanc', 'Lee Sin', 'Leona', 'Lillia', 'Lissandra', 'Lucian', 'Lulu', 'Lux', 'Malphite', 'Malzahar', 'Maokai', 'Master Yi', 'Milio', 'Miss Fortune', 'Wukong', 'Mordekaiser', 'Morgana', 'Nami', 'Nasus', 'Nautilus', 'Neeko', 'Nidalee', 'Nilah', 'Nocturne', 'Nunu & Willump', 'Olaf', 'Orianna', 'Ornn', 'Pantheon', 'Poppy', 'Pyke', 'Qiyana', 'Quinn', 'Rakan', 'Rammus', "Rek'Sai", 'Rell', 'Renata Glasc', 'Renekton', 'Rengar', 'Riven', 'Rumble', 'Ryze', 'Samira', 'Sejuani', 'Senna', 'Seraphine', 'Sett', 'Shaco', 'Shen', 'Shyvana', 'Singed', 'Sion', 'Sivir', 'Skarner', 'Sona', 'Soraka', 'Swain', 'Sylas', 'Syndra', 'Tahm Kench', 'Taliyah', 'Talon', 'Taric', 'Teemo', 'Thresh', 'Tristana', 'Trundle', 'Tryndamere', 'Twisted Fate', 'Twitch', 'Udyr', 'Urgot', 'Varus', 'Vayne', 'Veigar', "Vel'Koz", 'Vex', 'Vi', 'Viego', 'Viktor', 'Vladimir', 'Volibear', 'Warwick', 'Xayah', 'Xerath', 'Xin Zhao', 'Yasuo', 'Yone', 'Yorick', 'Yuumi', 'Zac', 'Zed', 'Zeri', 'Ziggs', 'Zilean', 'Zoe', 'Zyra']
        version_request = requests.get("https://ddragon.leagueoflegends.com/api/versions.json")
        if version_request.status_code == 200:
            version = version_request.json()[0]
            request = requests.get(f"http://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/champion.json")
            if request.status_code == 200:
                data = request.json()
                champs = [data["data"][champion]["name"] for champion in data["data"]]
            else:
                champs = hard_coded_champs
        else:
            champs = hard_coded_champs
    return champs[random.randint(0, len(champs) - 1)]
 
@app_commands.command(name="random", description="Get a random agent or champion")
async def random_agent(interaction: discord.Interaction, game: str):
    if not (game == "Valorant" or game == "League"):
        return await interaction.response.send_message("Invalid game, please choose between Valorant and League of Legends", ephemeral=True)
    await interaction.response.send_message(get_agent() if game == "Valorant" else get_champion())

@random_agent.autocomplete("game")
async def random_agent_game_autocomplete(interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
    return [
        app_commands.Choice(name="Valorant", value="Valorant"),
        app_commands.Choice(name="League of Legends", value="League"),
    ]