from PIL import ImageFont
import discord
from discord.ext import commands
import io

import os
import dotenv

from PIL import Image, ImageDraw


dotenv.load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
ADMIN_CHANNEL_ID = os.getenv("ADMIN_CHANNEL")

bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())
ADMIN_CHANNEL = bot.get_channel(int(ADMIN_CHANNEL_ID))

COLORS = {
    "R": (225, 29, 72),   # Crisp Red
    "B": (37, 99, 235),   # Royal Blue
    "G": (22, 163, 74),   # Emerald Green
    "P": (139, 92, 246),  # Purple
    "0": (255, 255, 255),   # White
    "GRID": (0, 0, 0),  # Black border

    "Y": (255, 251, 71),   # Golden Yellow for fallback
    
}

CELL_SIZE = 40
MAP_WIDTH, MAP_HEIGHT = CELL_SIZE * 20, CELL_SIZE * 18
COLOUR_LAYOUT = [
    "WWRGGGGGGGRWWRGGGGGGGRWW",
    "WWRGGGGGGGRWWRGGGGGGGRWW",
    "RRRGGGGGGGRRRRGGGGGGGRRR",
    "GGGGGGGGBBGGGGGBBGGGGGGG",
    "GGGGGGBBBBGGGGGBBBBGGGGG",
    "GGGGGBBBBBBGGGBBBBBBGGGG",
    "GGGGBBBBBGGGGGGGBBBBBGGG",
    "GGGGBBBBBKGGGGGKBBBBBGGG",
    "WWRGBBBBBKKKKKKKBBBBGRWW",
    "WWRGBBBBBKKKKKKKBBBBGRWW",
    "RRRGBBBBBKGGGGGKBBBBBRRR",
    "GGGGBBBBBGGGGGGGBBBBBGGG",
    "GGGGGBBBBBBGGGBBBBBBGGGG",
    "GGGGGGBBBBGGGGGBBBBGGGGG",
    "GGGGGGGGBBGGGGGBBGGGGGGG",
    "RRRGGGGGGGRRRRGGGGGGGRRR",
    "WWRGGGGGGGRWWRGGGGGGGRWW",
    "WWRGGGGGGGRWWRGGGGGGGRWW",
]

map = [[0] * 20 for _ in range(18)]



def drawMap():
    # initialise grid with empty value, white color
    grid_data = [[("0", "")] * 20 for _ in range(18)]

    # Create canvas
    img = Image.new("RGB", (MAP_WIDTH, MAP_HEIGHT), color=COLORS["0"])
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.load_default()
    except Exception:
        font = None

    # paint map
    for i in range(18):
        for j in range(20):
            color_code = COLOUR_LAYOUT[i][j]
            color = COLORS.get(color_code, COLORS["G"])
            
            x1, y1 = j * CELL_SIZE, i * CELL_SIZE
            x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
            
            # Draw cell background and subtle grid border
            draw.rectangle([x1, y1, x2 - 1, y2 - 1], fill=color, outline=COLORS["GRID"])
            
    

@bot.command()
async def map(ctx):
    pass

bot.run(TOKEN)