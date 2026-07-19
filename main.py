from PIL import ImageFont
import discord
from discord.ext import commands
import io

import os
import dotenv

from PIL import Image, ImageDraw


dotenv.load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
ADMIN_CHANNEL_IDS = os.getenv("ADMIN_CHANNEL").split(",")
ADMIN_CHANNEL_IDS = [int(ch_id) for ch_id in ADMIN_CHANNEL_IDS] #convert to int

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

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
    "1": (30, 255, 255), # colour for group 1, colour: Cyan
    "2": (34, 139, 130), # colour for group 2, colour: turtoise
    "3": (255, 193, 37), # colour for group 3, colour: magenta
    "4": (205, 127, 50),  # colour for group 4, colour: bronze
    "5": (255, 192, 203),  # colour for group 5, colour: pink
    "6": (168, 12, 184), # colour for group 6, colour: Purple
    "7": (255, 204, 102), # colour for group 7, colour: Orange
    "8": (186, 191, 196),  # colour for group 8, colour: silver
}

CELL_SIZE = 50
MAP_WIDTH, MAP_HEIGHT = CELL_SIZE * 20, CELL_SIZE * 18
COLOUR_LAYOUT = [
    #12345678901234567890
    "WWRGGGGGRWWRGGGGGRWW", #1
    "WWRGGGGGRWWRGGGGGRWW", #2
    "RRGGGBGGGRRGGGBGGGRR", #3
    "GGGGBBBGGGGGGBBBGGGG", #4
    "GGGBBBBBGGGGBBBBBGGG", #5
    "GGGBBBBBBGGBBBBBBGGG", #6
    "GGGGBBBBBBBBBBBBGGGG", #7
    "RRGGGBBBKBBKBBBGGGRR", #8
    "WWRGGGBBBKKBBBGGGRWW", #9
    "WWRGGGBBBKKBBBGGGRWW", #10
    "RRGGGBBBKBBKBBBGGGRR", #11
    "GGGGBBBBBBBBBBBBGGGG", #12
    "GGGBBBBBBGGBBBBBBGGG", #13
    "GGGBBBBBGGGGBBBBBGGG", #14
    "GGGGBBBGGGGGGBBBGGGG", #15
    "RRGGGBGGGRRGGGBGGGRR", #16
    "WWRGGGGGRWWRGGGGGRWW", #17
    "WWRGGGGGRWWRGGGGGRWW", #18
]

label_layout = [
    #12345678901234567890
    "11000000022000000033", #1
    "11000000022000000033", #2
    "00000000000000000000", #3
    "00000000000000000000", #4
    "00000000000000000000", #5
    "00000000000000000000", #6
    "00000000000000000000", #7
    "00000000000000000000", #8
    "44000000000000000055", #9
    "44000000000000000055", #10
    "00000000000000000000", #11
    "00000000000000000000", #12
    "00000000000000000000", #13
    "00000000000000000000", #14
    "00000000000000000000", #15
    "00000000000000000000", #16
    "66000000077000000088", #17
    "66000000077000000088", #18
]



def drawMap():
    """
    The function to generate the map.
    """
    # Create canvas
    img = Image.new("RGB", (MAP_WIDTH, MAP_HEIGHT), color=COLORS["W"])
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("Google.ttf", 30)
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
    """
    The command to generate the map.
    """
    msg = await ctx.send("Generating map...")

    img = drawMap()

    with io.BytesIO() as image_binary:
        img.save(image_binary, "PNG")
        image_binary.seek(0)
        await msg.edit(
            content="Map generated", 
            attachments=[discord.File(image_binary, "map.png")]
            )

@bot.command()
async def update(ctx, group: int, *coords: str):
    """
    The command to update the map. Only allowed in allowed channels
    """
    # check if sender is in allowed channel
    if ctx.channel.id not in ADMIN_CHANNEL_IDS:
        await ctx.send("Nice try but no.")
        return
    
    # check if group is valid
    if group not in [1,2,3,4,5,6,7,8]:
        await ctx.send("Invalid group number. Must be between 1 and 8")
        return
    
    # check for duplicates in coords
    if len(coords) != len(set(coords)):
        await ctx.send("Duplicate coordinates")
        return
    
    # parse coords and update the map
    msg = await ctx.send("Updating map...")
    

    for coord in coords:
        #convert coords eg. a1 -> (1,1), b2 -> (2,2), etc., 1-indexed
        x = ord(coord[0].lower()) - 96
        y = int(coord[1])
        
        try:
            # update label layout, label layout 0-indexed
            row = list(label_layout[x-1])
            row[y-1] = str(group)

            #convert back to string
            label_layout[x-1] = "".join(row)

        except:
            await ctx.send(f"Invalid coordinate: {coord}")
            return

    await msg.edit(content="OK")
    
    img = drawMap()
    with io.BytesIO() as image_binary:
        img.save(image_binary, "PNG")
        image_binary.seek(0)
        await ctx.send("Map updated", file=discord.File(image_binary, "map.png"))

    


if __name__ == "__main__":
    bot.run(TOKEN)