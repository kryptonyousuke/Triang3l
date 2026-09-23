#
# Copyright 2026 Krypton Yousuke.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import discord
import aioconsole
import typing
import secrets
import aiosqlite
from discord import app_commands

from database import database
from session import session_manager as session
from util.structs import colors, Group

class Triang3l(discord.ext.commands.Bot):
    @session.session
    def __init__(self, token: str, intents: discord.Intents):
        super().__init__(command_prefix="!", intents=intents)
        self.token = token
        self.setup_commands()
        self.db: database.Database | None = None

    @staticmethod
    def generate_hash() -> str:
        return secrets.token_hex(64)

    async def close(self):
        if self.db:
            await self.db.close()
            await aioconsole.aprint("Database connection closed successfully.")

    def setup_commands(self):
        ########################################
        #                 EVENTS               #
        ########################################

        @self.event
        async def on_ready():
            try:
                synced = await self.tree.sync()
                await aioconsole.aprint(f"Connected as {self.user} | {len(synced)} command(s) synchronized.")
                self.db = await database.Database.create("Triang3l.db")
            except Exception as e:
                await aioconsole.aprint(f"Failed to sync commands: {e}")

        @self.event
        async def on_disconnect():
            await aioconsole.aprint("Triang3l is now disconnected.")

        @self.event
        async def on_member_ban(guild: discord.Guild, user: discord.User):
            try:
                await aioconsole.aprint("Member banned!")
            except discord.Forbidden:
                pass


        ########################################
        #               COMMANDS               #
        ########################################

        @self.tree.command(name="ping", description="Show the latency.")
        async def ping(interaction: discord.Interaction):
            latency = round(self.latency * 1000)
            await interaction.response.send_message(f"Pong! Latency: {latency}ms")

        # Initial setup.
        @self.tree.command(name="setup", description="Register the current server into Triang3l database.")
        @app_commands.describe()
        async def setup(interaction: discord.Interaction):
            embed = discord.Embed()
            embed.color = colors.green
            embed.description = f"""
Server ID: {interaction.guild_id}
Successfully registered into Tr1angel.
"""
            await self.db.insert_server(interaction.guild.name, interaction.guild_id)
            await interaction.response.send_message(embed=embed)

        # Group handling.
        @self.tree.command(name="newgroup", description="Create a new group.")
        @app_commands.describe(
            group_name="Group name"
        )
        async def newgroup(interaction: discord.Interaction, group_name: str):
            embed = discord.Embed()
            try:
                hash = self.generate_hash()
                await self.db.create_group(group_name, interaction.guild_id, hash)
                embed.color = colors.green
                embed.description = f"Successfully registered `{group_name}` with the hash `{hash}`"
                await interaction.response.send_message(embed=embed)
            except aiosqlite.Error:
                embed.color = colors.red
                embed.description = "Database exception. Try to contact the bot admins."
                await interaction.response.send_message(embed=embed)


        @self.tree.command(name="listgroups", description="List all the groups this server is part of.")
        @app_commands.describe()
        async def listgroups(interaction: discord.Interaction):
            embed = discord.Embed()
            embed.title  = "Group List"
            embed.color = colors.white
            description = ""
            groups = []
            for group_info in await self.db.fetch_groups(interaction.guild_id):
                group = Group()
                group_details = await self.db.fetch_group_by_id(group_info["group_id"])
                group.group_name = group_details["name"]
                group.group_id = group_details["id"]
                group.group_hash = group_details["group_hash"]
                group.server_owner_id = group_details["server_owner_id"]
                group.server_owner_name = (await self.db.fetch_server_by_id(group_details["server_owner_id"]))["name"]
                group = group.all_valid()
                if group:
                    groups.append(group)
            for group in groups:
                description += f"{group['group_name']} — {group['server_owner_name']} — {group['group_hash']}\n"

            embed.description = description
            
            await interaction.response.send_message(embed=embed)


        @self.tree.command(name="joingroup", description="Request to join a group.")
        @app_commands.describe(
            group_hash="Group hash"
        )
        async def joingroup(interaction: discord.Interaction, group_hash: str):
            await interaction.response.send_message("Pong! Latency: ms")

        
        @self.tree.command(name="listjoinrequests", description="List servers that requested to join to one of your groups.")
        @app_commands.describe(
            group_hash="Group hash"
        )
        async def listjoinrequests(interaction: discord.Interaction, group_hash: str):
            await interaction.response.send_message("Pong! Latency: ms")

        
        @self.tree.command(name="rotategroupinvite", description="Rotate a group invite to a new hash.")
        @app_commands.describe(
            group_hash="Group hash"
        )
        async def rotategroupinvite(interaction: discord.Interaction, group_hash: str):
            await interaction.response.send_message("Pong! Latency: ms")

        
        @self.tree.command(name="acceptjoinrequest", description="Accept a join request by id.")
        @app_commands.describe(
            group_hash="Group hash",
            request_id="Request ID"
        )
        async def acceptjoinrequest(interaction: discord.Interaction, group_hash: str, request_id: int):
            await interaction.response.send_message("Pong! Latency: ms")


        # Moderation workflow commands.
        @self.tree.command(name="banlist", description="Show the ban list.")
        @app_commands.describe(
            group_hash="Group hash"
        )
        async def banlist(interaction: discord.Interaction, group_hash: str):
            await interaction.response.send_message("Pong! Latency: ms")

        
        @self.tree.command(name="accept", description="Accept a specific ban by id.")
        @app_commands.describe(
            group_hash="Group hash",
            punishment_id="Punishment Index"
        )
        async def accept(interaction: discord.Interaction, group_hash: str, punishment_id: int):
            await interaction.response.send_message("Pong! Latency: ms")

        
        @self.tree.command(name="acceptall", description="Accept all the bans marked as unreviewed.")
        @app_commands.describe(
            group_hash="Group hash"
        )
        async def acceptall(interaction: discord.Interaction, group_hash: str):
            await interaction.response.send_message("Pong! Latency: ms")

        
        @self.tree.command(name="listunreviewed", description="List all bans that needs review.")
        @app_commands.describe(
            group_hash="Group hash"
        )
        async def listunreviewed(interaction: discord.Interaction, group_hash: str):
            await interaction.response.send_message("Pong! Latency: ms")

        
        @self.tree.command(name="deny", description="Refuse a specific ban by id.")
        @app_commands.describe(
            group_hash="Group hash",
            punishment_id="Punishment Index"
        )
        async def deny(interaction: discord.Interaction, group_hash: str, punishment_id: int):
            await interaction.response.send_message("Pong! Latency: ms")

        
        @self.tree.command(name="finishreview", description="Synchronize bans (all of them must be marked as reviewed).")
        @app_commands.describe(
            group_hash="Group hash"
        )
        async def finishreview(interaction: discord.Interaction, group_hash: str):
            await interaction.response.send_message("Pong! Latency: ms")

        
        @self.tree.command(name="releasebanlist", description="Ends the current ban list and creates a new empty one.")
        @app_commands.describe(
            group_hash="Group hash"
        )
        async def releasebanlist(interaction: discord.Interaction, group_hash: str):
            await interaction.response.send_message("Pong! Latency: ms")
    def run_bot(self):
        self.run(self.token)
