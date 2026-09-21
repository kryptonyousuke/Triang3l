#
# Copyright 2026 Krypton Yousuke.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import discord
import aioconsole

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
                await aioconsole.aprint(f"Connected as {self.bot.user} | {len(synced)} command(s) synchronized.")
            except Exception as e:
                await aioconsole.aprint(f"Failed to sync commands: {e}")
 
        @self.bot.event
        async def on_disconnect():
            await aioconsole.aprint("Triang3l is now disconnected.")

        @self.bot.event
        async def on_member_ban(guild: discord.Guild, user: discord.User):
            try:
                await aioconsole.aprint("Member banned!")
            except discord.Forbidden:
                pass
        
        @self.bot.tree.command(name="ping", description="Show the latency.")
        async def ping(interaction: discord.Interaction):
            latency = round(self.bot.latency * 1000)
            await interaction.response.send_message(f"Pong! Latency: {latency}ms")

        """
        # Initial setup.
        @self.bot.tree.command(name="setup", description="Register the current server into Triang3l database.")

        # Group handling.
        @self.bot.tree.command(name="newgroup", description="Create a new group.")
        @self.bot.tree.command(name="listgroups", description="List all the groups this server is part of.")
        @self.bot.tree.command(name="joingroup", description="Request to join a group.")
        @self.bot.tree.command(name="listjoinrequests", description="List servers that requested to join to one of your groups.")
        @self.bot.tree.command(name="rotategroupinvite", description="Rotate a group invite to a new hash.")
        @self.bot.tree.command(name="acceptjoinrequest", description="Accept a join request by id.")
        

        # Moderation workflow commands.
        @self.bot.tree.command(name="banlist", description="Show the ban list.")
        @self.bot.tree.command(name="accept", description="Accept a specific ban by id.")
        @self.bot.tree.command(name="acceptall", description="Accept all the bans marked as unreviewed.")
        @self.bot.tree.command(name="listunreviewed", description="List all bans that needs review.")
        @self.bot.tree.command(name="deny", description="Refuse a specific ban by id.")
        @self.bot.tree.command(name="finishreview", description="Synchronize bans (all of them must be marked as reviewed).")
        @self.bot.tree.command(name="releasebanlist", description="Ends the current ban list and creates a new empty one.")
        """
        

    def run(self):
        self.bot.run(self.token)
   
 
