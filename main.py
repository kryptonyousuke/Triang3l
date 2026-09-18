#
# Copyright 2026 Krypton Yousuke.
#
# SPDX-License-Identifier: GPL-3.0-or-later
# 

import discord
from discord.ext import commands
from triang3l.triang3l import Triang3l

intents = discord.Intents.default()
intents.message_content = True
        
bot = commands.Bot(command_prefix="!", intents=intents)

if __name__ == '__main__':
    triang3l = Triang3l(intents=intents, bot=bot)
    triang3l.setup_commands()
    triang3l.run()
