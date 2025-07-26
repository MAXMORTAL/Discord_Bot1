import random
import asyncio
from discord.ext import commands

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.greetings = ["hello", "hi", "hey", "yo", "howdy", "greetings", "salutations", "hola", "ni hao", "wassup", "sup"]
        self.responses = ["Hello!", "Hi there!", "Hey!", "Yo!", "Howdy!", "Greetings!", "Salutations!", "Hola!", "Ni hao!", "Wassup!", "Sup!", "Good to see you!", "Hello there!"]
        self.bot.greeted_users = {}

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        msg = message.content.lower()
        user_id = message.author.id
        words = msg.split()
        cleaned_words = [''.join(char for char in word if char.isalpha()) for word in words]

        if any(word in self.greetings for word in cleaned_words):
            if self.bot.greeted_users.get(user_id, False):
                return

            response = random.choice(self.responses)
            await message.channel.send(f"{response} {message.author.display_name}")
            self.bot.greeted_users[user_id] = asyncio.get_event_loop().time()

            asyncio.create_task(self.reset_greeted_user(user_id))

    async def reset_greeted_user(self, user_id):
        await asyncio.sleep(5 * 60 * 60)
        if user_id in self.bot.greeted_users:
            del self.bot.greeted_users[user_id]

async def setup(bot):
    await bot.add_cog(General(bot))
