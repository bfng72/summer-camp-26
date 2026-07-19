from PIL import Image, ImageDraw, ImageFont


def drawMap(MAP_WIDTH, MAP_HEIGHT, COLORS, LABEL_COLORS, CELL_SIZE, COLOUR_LAYOUT, label_layout, village_coords):
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

    # Draw header corner cell
    draw.rectangle([0, 0, CELL_SIZE - 1, CELL_SIZE - 1], fill=COLORS["GREY"], outline=COLORS["GRID"])

    # Draw X-axis labels (1 to 20) on top row
    for j in range(1, 21):
        x1, y1 = j * CELL_SIZE, 0
        x2, y2 = x1 + CELL_SIZE, CELL_SIZE
        draw.rectangle([x1, y1, x2 - 1, y2 - 1], fill=COLORS["GREY"], outline=COLORS["GRID"])
        draw.text((x1 + CELL_SIZE/2, y1 + CELL_SIZE/2), str(j), fill=COLORS["K"], anchor="mm", font=font)

    # Draw Y-axis labels (A to R) on left column
    for i in range(1, 19):
        x1, y1 = 0, i * CELL_SIZE
        x2, y2 = CELL_SIZE, y1 + CELL_SIZE
        label_letter = chr(64 + i) # 65 is 'A'
        draw.rectangle([x1, y1, x2 - 1, y2 - 1], fill=COLORS["GREY"], outline=COLORS["GRID"])
        draw.text((x1 + CELL_SIZE/2, y1 + CELL_SIZE/2), label_letter, fill=COLORS["K"], anchor="mm", font=font)

    # Draw actual map cells
    for i in range(18): #y axis
        for j in range(20): #x axis
            # paint map
            color_code = COLOUR_LAYOUT[i][j]
            color = COLORS.get(color_code, COLORS["G"])
            
            # Offset by 1 cell size to leave room for labels
            x1, y1 = (j + 1) * CELL_SIZE, (i + 1) * CELL_SIZE
            x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
            
            # Draw cell background and subtle grid border
            draw.rectangle([x1, y1, x2 - 1, y2 - 1], fill=color, outline=COLORS["GRID"])

            # labels
            raw_label = label_layout[i][j]
            label_code = f"{raw_label}V" if (i, j) in village_coords else raw_label
            if raw_label != "0":
                x, y = x1 + (CELL_SIZE/2), y1 + (CELL_SIZE/2)
                draw.text(
                    (x, y), 
                    label_code, 
                    fill=LABEL_COLORS.get(raw_label, COLORS["GRID"]), 
                    stroke_width=2, 
                    stroke_fill=COLORS["GRID"], 
                    anchor="mm",
                    font=font
                    )

    return img


def convertCoord(coord: str):
    x = ord(coord[0].lower()) - 96
    y = int(coord[1:]) # Support multi-digit columns like a10
    
    return (x-1, y-1)