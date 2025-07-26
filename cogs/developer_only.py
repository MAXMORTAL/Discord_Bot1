import discord
from discord.ext import commands
import time
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

DEV_ROLE_NAMES = [role.strip().lower() for role in os.getenv("DEV_ROLE_NAMES", "").split(",")]
BOT_OWNER_ID = int(os.getenv("BOT_OWNER_ID", "0"))

def is_dev(ctx):
    return (
        ctx.author.id == BOT_OWNER_ID or
        any(role.name.lower() in DEV_ROLE_NAMES for role in ctx.author.roles)
    )

class DeveloperOnly(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="cooldowns")
    async def check_cooldowns(self, ctx):
        if not is_dev(ctx):
            await ctx.send("❌ You don't have permission to use this command.")
            return

        embed = discord.Embed(
            title="🕒 Users on Cooldown",
            color=discord.Color.red()
        )

        if not hasattr(self.bot, "greeted_users") or not self.bot.greeted_users:
            embed.description = "No users are on cooldown currently."
        else:
            now = asyncio.get_event_loop().time()
            count = 0

            for user_id, start_time in self.bot.greeted_users.items():
                remaining = int(5 * 60 * 60 - (now - start_time))
                if remaining <= 0:
                    continue

                member = ctx.guild.get_member(user_id)
                name = member.display_name if member else "Unknown User"

                hours, rem = divmod(remaining, 3600)
                minutes, seconds = divmod(rem, 60)

                embed.add_field(
                    name=name,
                    value=f"{hours}h {minutes}m {seconds}s remaining",
                    inline=False
                )
                count += 1

            if count == 0:
                embed.description = "No users are on cooldown currently."

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(DeveloperOnly(bot))
