import discord
import os
import riot
from discord import app_commands

intents = discord.Intents.default()
client = discord.Client(intents=intents)
command_tree = app_commands.CommandTree(client)

command_tree.add_command(riot.random_agent)

@client.event
async def on_ready():
    await command_tree.sync()
    print("Ready :)")
    
@command_tree.command(name="help", description="Get a list of all commands")
async def help(interaction: discord.Interaction):
    commands = {}
    for command in command_tree.get_commands():
        commands[command.name] = command.description
    message = "Commands: \n"
    for command in commands:
        message += f"/{command} - {commands[command]}\n"
    await interaction.response.send_message(message)

client.activity = discord.Activity(type=discord.ActivityType.listening, name="/help")
client.run(os.environ["BotToken"])