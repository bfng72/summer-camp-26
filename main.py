import discord
from discord.ext import commands
import io

import os
import dotenv

from PIL import Image, ImageDraw


dotenv.load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())

COLORS = {
    "R": (225, 29, 72),   # Crisp Red
    "B": (37, 99, 235),   # Royal Blue
    "G": (22, 163, 74),   # Emerald Green
    "P": (139, 92, 246),  # Purple
    "0": (255, 255, 255),   # White (Empty)
    "GRID": (0, 0, 0)  # Black border
}

CELL_SIZE = 40
MAP_WIDTH, MAP_HEIGHT = CELL_SIZE * 8, CELL_SIZE * 8


def drawMap():
    # initialise grid with empty value, white color
    grid_data = [[("0", "")] * 20 for _ in range(10)]
    

@bot.command()
async def map(ctx):
    pass

bot.run(TOKEN)