import typer
from pathlib import Path
import numpy as np
import cv2
import math

app = typer.Typer()

class Vertice:
    def __init__(self, label: str):
        self.label = label
        self.status = 0

    def set_status(self, status: int):
        self.status = status

def find_by_status(list: list[Vertice], status: int):
    for item in list:
        if (item.status == status): return item, list.index(item)

    return None

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

    vertice_acc = 1
    vertice_list = []

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
            font_scale = 3
            font_thickness = 6
            
            box_size = 177
            border_thickness = 4
            color = (0, 0, 0)

            # rb (right-bottom)
            if ((c + 1) < col_size and (r + 1) < row_size):
                vertice = Vertice(str(vertice_acc))
                vertice.set_status(2)
                vertice_list.append(vertice)

                top_left = (FWIDTH - box_size, FHEIGHT - box_size)
                bottom_right = (FWIDTH, FHEIGHT)
                cv2.rectangle(bordered_image, top_left, bottom_right, color, border_thickness)

                bordered_image = cv2.putText(bordered_image, vertice.label,
                                            (top_left[0] + 20, bottom_right[1] - 20),
                                            font, font_scale, color, font_thickness, cv2.LINE_AA)

            # lb (left-bottom)
            if (c > 0 and (r + 1) < row_size):
                vertice, idx = find_by_status(vertice_list, 2)
                vertice_list[idx].set_status(3)

                top_left = (0, FHEIGHT - box_size)
                bottom_right = (box_size, FHEIGHT)
                cv2.rectangle(bordered_image, top_left, bottom_right, color, border_thickness)

                bordered_image = cv2.putText(bordered_image, vertice.label,
                                            (top_left[0] + 20, bottom_right[1] - 20),
                                            font, font_scale, color, font_thickness, cv2.LINE_AA)

            # rt (right-top)
            if ((c + 1) < col_size and r > 0):
                vertice, idx = find_by_status(vertice_list, 3)
                vertice_list[idx].set_status(4)

                top_left = (FWIDTH - box_size, 0)
                bottom_right = (FWIDTH, box_size)
                cv2.rectangle(bordered_image, top_left, bottom_right, color, border_thickness)

                bordered_image = cv2.putText(bordered_image, vertice.label,
                                            (top_left[0] + 20, top_left[1] + box_size - 20),
                                            font, font_scale, color, font_thickness, cv2.LINE_AA)

            # lt (left-top)
            if (c > 0 and r > 0):
                vertice, idx = find_by_status(vertice_list, 4)
                vertice_list[idx].set_status(5)

                top_left = (0, 0)
                bottom_right = (box_size, box_size)
                cv2.rectangle(bordered_image, top_left, bottom_right, color, border_thickness)

                bordered_image = cv2.putText(bordered_image, vertice.label,
                                            (top_left[0] + 20, top_left[1] + box_size - 20),
                                            font, font_scale, color, font_thickness, cv2.LINE_AA)
            vertice_acc += 1

            cv2.imwrite(f"out/{r+1}{c+1}_out.jpg", bordered_image)

if __name__ == "__main__":
    app()