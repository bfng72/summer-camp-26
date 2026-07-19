import discord
from discord.ext import commands
import io
import datetime as dt
import json

import os
import dotenv

import helpers


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
    "GREY": (186, 191, 196), # Grey for axis
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
MAP_WIDTH, MAP_HEIGHT = CELL_SIZE * (20+1), CELL_SIZE * (18+1)
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

village_coords = set()


# save data to text file
def save_data():
    try:
        with open("autosave.json", "w") as f:
            json.dump({
                "label_layout": label_layout,
                "village_coords": list(village_coords),
                "last_update": dt.datetime.now().strftime("%H:%M:%S")
            }, f, indent=4)
        print("Autosave complete: autosave.json")
    except Exception as e:
        print(f"Autosave failed: {e}")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")



###
             

@bot.command()
async def map(ctx):
    """
    The command to generate the map.
    """
    msg = await ctx.send("Generating map...")

    img = helpers.drawMap(MAP_WIDTH, MAP_HEIGHT, COLORS, LABEL_COLORS, CELL_SIZE, COLOUR_LAYOUT, label_layout, village_coords)

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
    if group not in [0,1,2,3,4,5,6,7,8]:
        await ctx.send("ERROR: Invalid group number. Must be between 1 and 8")
        return
    
    # check for duplicates in coords
    if len(coords) != len(set(coords)):
        await ctx.send("ERROR: Duplicate coordinates")
        return
    
    # parse coords and update the map
    msg = await ctx.send("Updating map...")
    
    if group == 0:
        #remove number or village in cell
        for coord in coords:
            try:
                (x, y) = helpers.convertCoord(coord)
                
                # if there is village on coord, remove it only
                if (x, y) in village_coords:
                    village_coords.remove((x, y))
                else:
                    row = list(label_layout[x])
                    row[y] = "0"
                    label_layout[x] = "".join(row)
            except:
                await ctx.send(f"ERROR: Invalid coordinate: {coord}")
                await msg.delete()
                return

    else:
        for coord in coords:
            try:
                (x, y) = helpers.convertCoord(coord)
                
                #if coord has number, add the coord to village_coords
                if label_layout[x][y] != "0":
                    #if coord color code is K, allow adding village
                    if COLOUR_LAYOUT[x][y] == "K":
                        if (x, y) in village_coords:
                            await ctx.send(f"ERROR: {coord} already has a village.")
                            await msg.delete()
                            return
                        else:
                            village_coords.add((x, y))
                    else:
                        await ctx.send(f"ERROR: Cannot build village in this coordinate: {coord}.")
                        await msg.delete()
                        return
                else:
                    row = list(label_layout[x])
                    row[y] = str(group)
                    label_layout[x] = "".join(row)
            except:
                await ctx.send(f"ERROR: Invalid coordinate: {coord}")
                await msg.delete()
                return

    save_data()

    await msg.edit(content="OK")
    
    img = helpers.drawMap(MAP_WIDTH, MAP_HEIGHT, COLORS, LABEL_COLORS, CELL_SIZE, COLOUR_LAYOUT, label_layout, village_coords)
    with io.BytesIO() as image_binary:
        img.save(image_binary, "PNG")
        image_binary.seek(0)
        await ctx.send("Map updated", file=discord.File(image_binary, "map.png"))

    


if __name__ == "__main__":
    bot.run(TOKEN)