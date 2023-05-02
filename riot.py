import os
import json
import requests
import random
import discord
from discord import app_commands
from typing import Optional

agents = {}
champs = []

def get_agent(role):
    global agents
    if agents == {}:
        with open("agents.json", "r") as f:
            agents = json.load(f)
    agents_in_role = agents[role]
    return agents_in_role[random.randint(0, len(agents_in_role) - 1)]

def get_champion(): #TODO: Find a way to sort champions by role
    global champs
    if champs == []:
        with open("champions.json", "r") as f:
            champs = json.load(f)
    return champs[random.randint(0, len(champs) - 1)]
 
@app_commands.command(name="random", description="Get a random agent or champion")
async def random_agent(interaction: discord.Interaction, game: str, role: Optional[str]):
    if not (game == "Valorant" or game == "League"):
        return await interaction.response.send_message("Invalid game, please choose between Valorant and League of Legends", ephemeral=True)
    if role == None:
        role = "None"
    if game == "Valorant" and not (role == "Duelist" or role == "Controller" or role == "Sentinel" or role == "Initiator" or role == "None"):
        return await interaction.response.send_message(f"Invalid role \"{role}\", please choose between Duelist, Controller, Sentinel, Initiator, and None", ephemeral=True)
    await interaction.response.send_message(get_agent(role) if game == "Valorant" else get_champion())

@random_agent.autocomplete("game")
async def random_agent_game_autocomplete(interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
    return [
        app_commands.Choice(name="Valorant", value="Valorant"),
        app_commands.Choice(name="League of Legends", value="League"),
    ]

@random_agent.autocomplete("role")
async def random_agent_role_autocomplete(interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
    game = interaction.data["options"][0]["value"]
    if game == "League":
        return []
    
    roles = ["Duelist","Controller","Sentinel","Initiator"]
    return [
        app_commands.Choice(name=role, value=role) for role in roles if current.lower() in role.lower()
    ]