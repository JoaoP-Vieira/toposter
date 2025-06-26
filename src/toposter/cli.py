import typer
from pathlib import Path
import numpy as np
import cv2
import math

app = typer.Typer()

@app.command()
def toposter(path: Path):
    """Reads and prints basic info about an image file."""
    if not path.exists():
        typer.echo(f"File not found: {path}")
        raise typer.Exit(code=1)

    image = cv2.imread(str(path))
    if image is None:
        typer.echo("Error reading the image file.")
        raise typer.Exit(code=1)

    A4WIDTH = 2480
    A4HEIGHT = 3508

    XBORDER = 236
    YBORDER = 236

    IWIDTH = image.shape[1]
    IHEIGHT = image.shape[0]

    FWIDTH = A4WIDTH - XBORDER * 2
    FHEIGHT = A4HEIGHT - YBORDER * 2

    col_size = math.ceil(IWIDTH / (FWIDTH))
    row_size = math.ceil(IHEIGHT / (FHEIGHT))

    height_acc = 0

    for r in range(row_size):
        y0 = height_acc
        height_acc = height_acc + FHEIGHT
        y1 = height_acc

        width_acc = 0

        for c in range(col_size):
            x0 = width_acc
            width_acc = width_acc + FWIDTH
            x1 = width_acc

            tile = image[y0:y1, x0:x1]

            white_bg = 255 * np.ones((FHEIGHT, FWIDTH, 3), dtype=np.uint8)

            tile_height, tile_width = tile.shape[:2]

            white_bg[:tile_height, :tile_width] = tile

            cropped_image = white_bg

            bordered_image = cv2.copyMakeBorder(
                src=cropped_image,
                top=4,
                bottom=4,
                left=4,
                right=4,
                borderType=cv2.BORDER_CONSTANT,
                value=[0, 0, 0]
            )

            font = cv2.FONT_HERSHEY_COMPLEX_SMALL
            font_scale = 4
            font_thickness = 8
            text_color = (0, 0, 0)

            # lt
            if (c > 0 and r > 0):
                bordered_image = cv2.putText(bordered_image, f"{r+1}{c+1}", (50, 100), font, font_scale, text_color, font_thickness, cv2.LINE_AA)

            # rt
            if ((c + 1) < col_size and r > 0):
                bordered_image = cv2.putText(bordered_image, f"{r+1}{c+1}", (FWIDTH - 150, 100), font, font_scale, text_color, font_thickness, cv2.LINE_AA)

            # lb
            if (c > 0 and (r + 1) < row_size):
                bordered_image = cv2.putText(bordered_image, f"{r+1}{c+1}", (50, FHEIGHT - 50), font, font_scale, text_color, font_thickness, cv2.LINE_AA)

            # rb
            if ((c + 1) < col_size and (r + 1) < row_size):
                bordered_image = cv2.putText(bordered_image, f"{r+1}{c+1}", (FWIDTH - 150, FHEIGHT - 50), font, font_scale, text_color, font_thickness, cv2.LINE_AA)

            cv2.imwrite(f"out/{r+1}{c+1}_out.jpg", bordered_image)

if __name__ == "__main__":
    app()