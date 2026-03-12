from rich.console import Console
from rich.logging import RichHandler
import logging
import os

console = Console()

def setup_logger(log_dir):
    os.makedirs(log_dir, exist_ok=True)
    logging.basicConfig(
        level="INFO",
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True), logging.FileHandler(os.path.join(log_dir, "errors.log"))]
    )

def log_info(message):
    console.print(f"[bold blue][+][/bold blue] {message}")

def log_success(message):
    console.print(f"[bold green][✔][/bold green] {message}")

def log_error(message):
    console.print(f"[bold red][![/bold red] {message}")

def log_warn(message):
    console.print(f"[bold yellow][?][/bold yellow] {message}")
