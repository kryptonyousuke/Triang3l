#
# Copyright 2026 Krypton Yousuke.
#
# SPDX-License-Identifier: GPL-3.0-or-later
# 

import discord
from discord.ext import commands
from triang3l.triang3l import Triang3l

intents = discord.Intents.all()        

if __name__ == '__main__':
    triang3l = Triang3l(intents=intents)
    triang3l.run_bot()
    print("Bot is down.")
