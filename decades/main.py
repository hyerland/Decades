import typer
import logging
from typing_extensions import Annotated
from rich.logging import RichHandler

#* Setup logging and typer application

app = typer.Typer(add_completion=False)

FORMAT = "%(message)s"
logging.basicConfig(
    level="ERROR", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)

log = logging.getLogger("rich")


@app.callback()
def callback(verbose: Annotated[bool, typer.Option("-v", "--verbose", help="Adds verbose output to commands.")] = False):
    """
    A CLI tool to save recovery snapshots of your projects or files. ⌚
    """
    if verbose:
        log.setLevel(logging.DEBUG)

#TODO: Code functionality for `decades snap` command.
@app.command()
def snap():
    """
    Take the current specified project directory and save it as a snapshot to `.decades` directory.
    """
    typer.echo("Shooting portal gun")

