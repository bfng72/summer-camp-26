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

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
ADMIN_CHANNEL = bot.get_channel(int(ADMIN_CHANNEL_ID))

COLORS = {
    "R": (225, 29, 72),   # Crisp Red
    "G": (22, 163, 74),   # Emerald Green
    "B": (37, 99, 235),   # Royal Blue
    "W": (255, 255, 255),   # White
    "K": (0, 0, 0),         # Black (from layout)
    "GRID": (0, 0, 0),      # Black border
    "Y": (255, 251, 71),    # Golden Yellow for fallback
}

LABEL_COLORS = {
    "A": (30, 255, 255), # colour for group 1, colour: Cyan
    "B": (34, 139, 130), # colour for group 2, colour: turtoise
    "C": (255, 193, 37), # colour for group 3, colour: magenta
    "D": (127, 255, 0),  # colour for group 4, colour: chartreuse
    "E": (50, 205, 50),  # colour for group 5, colour: lime
    "F": (168, 12, 184), # colour for group 6, colour: Purple
    "G": (255, 204, 102), # colour for group 7, colour: Orange
}

CELL_SIZE = 50
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

label_layout = [
    "AA0000000000000000CC",
    "AA0000000000000000CC",
    "00000000000000000000",
    "00000000000000000000",
    "00000000000000000000",
    "00000000000000000000",
    "00000000000000000000",
    "00000000000000000000",
    "00000000000000000000",
    "00000000000000000000",
    "00000000000000000000",
    "00000000000000000000",
    "00000000000000000000",
    "00000000000000000000",
    "00000000000000000000",
    "00000000000000000000",
    "00000000000000000000",
    "00000000000000000000",
]



def drawMap():
    # Create canvas
    img = Image.new("RGB", (MAP_WIDTH, MAP_HEIGHT), color=COLORS["W"])
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("Google.ttf", 25)
    except Exception:
        font = None


    for i in range(18): #y axis
        for j in range(20): #x axis
            # paint map
            color_code = COLOUR_LAYOUT[i][j]
            color = COLORS.get(color_code, COLORS["G"])
            
            x1, y1 = j * CELL_SIZE, i * CELL_SIZE
            x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
            
            # Draw cell background and subtle grid border
            draw.rectangle([x1, y1, x2 - 1, y2 - 1], fill=color, outline=COLORS["GRID"])


            # labels
            label_code = label_layout[i][j]
            if label_code != "0":
                x, y = j * CELL_SIZE + (CELL_SIZE/2), i * CELL_SIZE + (CELL_SIZE/2)
                draw.text(
                    (x, y), 
                    label_code, 
                    fill=LABEL_COLORS.get(label_code, COLORS["GRID"]), 
                    stroke_width=2, 
                    stroke_fill=COLORS["GRID"], 
                    anchor="mm",
                    font=font
                    )

    return img
            
    

@bot.command()
async def map(ctx):
    msg = await ctx.send("Generating map...")

    img = drawMap()

    with io.BytesIO() as image_binary:
        img.save(image_binary, "PNG")
        image_binary.seek(0)
        await msg.edit(
            content="Map generated", 
            attachments=[discord.File(image_binary, "map.png")]
            )


if __name__ == "__main__":
    bot.run(TOKEN)