#
# Copyright 2026 Krypton Yousuke.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import discord
from session import session_manager as session

class Triang3l:
    @session.session
    def __init__(self, token: str, intents: discord.Intents, bot: discord.Bot):
        self.token = token
        self.bot = bot
        self.intents = intents

    def setup_commands(self):
        @self.bot.event
        async def on_ready():
            try:
                synced = await self.bot.tree.sync()
                print(f"Connected as {self.bot.user} | {len(synced)} command(s) synchronized.")
            except Exception as e:
                print(f"Falha ao sincronizar comandos: {e}")
        
        @self.bot.tree.command(name="ping", description="Show the latency.")
        async def ping2(interaction: discord.Interaction):
            latency = round(self.bot.latency * 1000)
            await interaction.response.send_message(f"Pong! Latency: {latency}ms")

    def run(self):
        self.bot.run(self.token)
   
