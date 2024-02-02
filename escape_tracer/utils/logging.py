from rich.console import Console
from rich.table import Table
from rich.prompt import Confirm, IntPrompt
from rich import print as rprint

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
    
def ask_signal_confirmation():
    
    is_signal_okay = Confirm.ask("Was signal read succesfully?")
    
    return is_signal_okay
    
def new_signal_attributes(old_threshold, old_start_skip, old_end_skip):
    
    rprint("Previous attributes: threshold: {}, start_skip: {}, end_skip: {}".format(old_threshold, old_start_skip, old_end_skip))

    new_threshold = IntPrompt.ask("Enter new threshold", default=old_threshold)
    new_start_skip = IntPrompt.ask("Enter new start_skip", default=old_start_skip)
    new_end_skip = IntPrompt.ask("Enter new end_skip", default=old_end_skip)
    
    return new_threshold, new_start_skip, new_end_skip