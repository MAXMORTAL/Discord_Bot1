import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from keep_alive import keep_alive

keep_alive()
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents, case_insensitive=True)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"{bot.user} is ready and online!")
    await bot.load_extension("cogs.general")
    await bot.load_extension("cogs.developer_only")


print("Web server is live at: https://your-repl-name.username.repl.co")
print("Token loaded:", os.getenv("TOKEN")[:10], "..." if os.getenv("TOKEN") else "MISSING")

bot.run(os.getenv("TOKEN"))
