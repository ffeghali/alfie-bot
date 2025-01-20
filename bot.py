import discord
from discord.ext import commands
import cogs.bot_commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)
# Load all cogs from the 'cogs' directory
# Add more cogs when more features added
COGS = ["bot_commands"]

@bot.event
async def on_ready():
    print(f"Bot is ready as {bot.user.name}")
    try:
        for cog in COGS:
            await bot.load_extension(f"cogs.{cog}")
        print("Cogs loaded successfully!")
    except Exception as e:
        print(f"Error loading cog: {e}")