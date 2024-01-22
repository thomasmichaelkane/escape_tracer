from rich.console import Console
from rich.table import Table

def display_coords(signalc, exitc):
    
    console = Console()
    console.print("-------------------------", style="magenta")
    
    signalc_str = [str(c) for c in signalc]
    exitc_str = [str(c) for c in exitc]
    
    table = Table(title="Video Segmentation Coordinates")

    table.add_column("Location", style="cyan")
    table.add_column("X", style="magenta", justify="right")
    table.add_column("Y", style="magenta", justify="right")

    table.add_row("Signal", signalc_str[0], signalc_str[1])
    table.add_row("Exit", exitc_str[0], exitc_str[1])

    
    console.print(table)