import typer
import logging
import os
import shutil
import json
from typing_extensions import Annotated, Optional
from rich import print
from rich.prompt import Confirm
from rich.logging import RichHandler
from rich.prompt import Prompt
from rich.table import Table

#* Setup logging and typer application

app = typer.Typer(add_completion=False)

FORMAT = "%(message)s"
logging.basicConfig(
    level="ERROR", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)

log = logging.getLogger("rich")

root = os.path.expanduser('~')

@app.callback()
def callback(verbose: Annotated[bool, typer.Option("-v", "--verbose", help="Adds verbose output to commands.")] = False,
             rebuild: Annotated[bool, typer.Option("-r", "--rebuild", help="Recreate everything.")] = False):
    """
    A CLI tool to save recovery snapshots of your projects or files. ⌚
    """
    if verbose:
        log.setLevel(logging.DEBUG)

    
    if rebuild:
        confirm = Confirm.ask("[red]Are you sure you want to rebuild?", default=False)
        if confirm:
            if os.path.exists(f"{root}/.decades"):
                shutil.rmtree(f"{root}/.decades")
            os.makedirs(f"{root}/.decades")
            with open(f"{root}/.decades/files.json", "w") as f:
                json.dump([], f, indent=4)
            if not os.path.exists(f"{root}/.decades/snapshots"):
                log.debug("Creating snapshots directory...")
                os.makedirs(f"{root}/.decades/snapshots")
            if not os.path.exists(f"{root}/.decades/config.json"):
                log.debug("Creating config.json...")
                with open(f"{root}/.decades/config.json", "w") as f:
                    json.dump({}, f, indent=4)
        else:
            print("[dim]Aborted.[/dim]")

    if not os.path.exists(f"{root}/.decades"):
        log.debug("Creating .decades directory...")
        os.makedirs(f"{root}/.decades")
    
    if not os.path.exists(f"{root}/.decades/files.json"):
        log.debug("Creating files.json...")
        with open(f"{root}/.decades/files.json", "w") as f:
            json.dump([], f, indent=4)
    
    if not os.path.exists(f"{root}/.decades/snapshots"):
        log.debug("Creating snapshots directory...")
        os.makedirs(f"{root}/.decades/snapshots")

    if not os.path.exists(f"{root}/.decades/config.json"):
        log.debug("Creating config.json...")
        with open(f"{root}/.decades/config.json", "w") as f:
            json.dump({}, f, indent=4)


@app.command()
def snap(
    file: Annotated[Optional[str], typer.Option("-f", "--file", help="File to save snapshot of.")] = None,
    encrypt: Annotated[bool, typer.Option("-e", "--encrypt", help="Encrypt the snapshot.", hidden=True)] = False,
) -> None:
    """
    Take the current active project directory or specified file and save it as a snapshot to `.decades` directory.
    """
    log.debug("Beginning check if is file or directory...")
    if file is None:
        log.debug("File not specified. Taking snapshot of current directory.")
        file = os.getcwd()
    else:
        log.debug("File specified. Taking snapshot of file.")
        log.debug("Checking if file exists...")
        path = os.path.join(os.getcwd(), file)
        if os.path.isdir(path):
            log.debug("Specified file is a directory.")
        elif os.path.isfile(path):
            log.debug("Specified file is a file.")
            file = os.path.basename(file)
        else:
            log.error(f"File, {file} does not exist.")
            exit(1)
            
    confirm = Confirm.ask("Are you sure you want to take a snapshot?", default=True)

    if confirm:
        print("[dim]Now add metadata to the snapshot.\n")

        name = Prompt.ask("What is the [yellow]name[/yellow] of the snapshot?")
        try:
            shutil.copytree(file, f"{root}/.decades/snapshots/{name}", copy_function=shutil.copy2, ignore=shutil.ignore_patterns('.git', '.venv'))
        except FileExistsError:
            log.error("Snapshot with the same name already exists.")
            exit(1)
        
        with open(f"{root}/.decades/files.json", "r") as f:
            files = json.load(f)
        
        files.append({
            "name": name,
            "path": f"{root}/.decades/snapshots/{name}",
        })

        with open(f"{root}/.decades/files.json", "w") as f:
            json.dump(files, f, indent=4)
            f.close()

        print("[green]Snapshot created! :sunglasses: [dim]Saved to 'files.json'")
    else:
        log.error("Snapshot cancelled.")
        exit(1)
    
    print("[green]Done! :sunglasses:")


@app.command()
def gallery():
    """
    View all snapshots in the `.decades` directory.
    """
    with open(f"{root}/.decades/files.json", "r") as f:
        files = json.load(f)
        
        table = Table(show_header=True, header_style="bold")
        table.add_column("#", style="dim", width=3)
        table.add_column("Name", style="bold", width=10)
        table.add_column("Path", style="dim", width=40)
        
        for i, file in enumerate(files):
            table.add_row(str(i), f"[blue]{file["name"]}", f"[yellow]{file["path"]}")
        
        print(table)
        choices = [str(i) for i in range(len(files))]
        choice = Prompt.ask("Which snapshot would you like to use? (Press Enter to exit)", choices=choices, default=None)
        if choice is None:
            print("Exiting choice list.")
        else:
            chosen = files[int(choice)]
            path = os.path.join(os.getcwd(), chosen['name'])
            shutil.copytree(chosen['path'], path, copy_function=shutil.copy2, ignore=shutil.ignore_patterns('.git', '.venv'))
            print(f"Snapshot cloned to {path}.")

