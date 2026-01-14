"""
CLI Entry Point for API Toolkit
"""
import click
from rich.console import Console

console = Console()


@click.group()
@click.version_option(version="0.1.0")
def cli() -> None:
    """
    🚀 API Toolkit - CLI para desarrolladores
    
    Herramienta para testing de APIs, gestión de colecciones,
    monitoreo de servicios y más.
    """
    pass


@cli.command()
def hello() -> None:
    """Comando de prueba para verificar instalación"""
    console.print("[bold green]✓[/bold green] API Toolkit está funcionando!")
    console.print("Usa [cyan]api-toolkit --help[/cyan] para ver todos los comandos")


if __name__ == "__main__":
    cli()