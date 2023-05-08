import json
import random
import discord
from discord import app_commands
from typing import Optional

agents = {}

with open("agents.json", "r") as f:
    agents = json.load(f)

# Add a None role to each game that includes all roles
for game in agents:
    agents[game]["None"] = []
    for role in agents[game]:
        agents[game]["None"] += agents[game][role]

def get_agent(game, role):
    global agents
    agents_in_role = agents[game][role]
    return agents_in_role[random.randint(0, len(agents_in_role) - 1)]
 
@app_commands.command(name="random", description="Get a random agent or champion")
async def random_agent(interaction: discord.Interaction, game: str, role: Optional[str]):
    if not game in agents:
        return await interaction.response.send_message("Invalid game", ephemeral=True)

    if role == None:
        role = "None"
    
    if not role in agents[game]:
        return await interaction.response.send_message(f"Invalid role \"{role}\"", ephemeral=True)

    await interaction.response.send_message(get_agent(game, role))

@random_agent.autocomplete("game")
async def random_agent_game_autocomplete(interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
    return [
        app_commands.Choice(name=Game, value=Game) for Game in agents if current.lower() in Game.lower()
    ]

@random_agent.autocomplete("role")
async def random_agent_role_autocomplete(interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
    game = interaction.data["options"][0]["value"]
    if not game in agents: 
        return []
    
    roles = list(agents[game].keys())
    for role in roles:
        if role == "None":
            roles.remove(role)
            break
    return [
        app_commands.Choice(name=role, value=role) for role in roles if current.lower() in role.lower()
    ]
