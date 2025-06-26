import typer
import cv2
from typing_extensions import Annotated

def toposter(
    path: Annotated[str, typer.Argument(help="Input file path")] = ""
):
    """
    Loads and displays basic info of an image file.
    """
    if not path.exists():
        typer.echo(f"Error: File '{path}' does not exist.", err=True)
        raise typer.Exit(code=1)

    image = cv2.imread(str(path))

    if image is None:
        typer.echo(f"Error: Unable to read image from '{path}'.", err=True)
        raise typer.Exit(code=1)

    typer.echo(f"Image loaded successfully: {path}")
    typer.echo(f"Image shape: {image.shape}")
