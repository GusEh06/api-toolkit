"""
Comandos para hacer requests HTTP
"""
from typing import Optional

import click
import httpx
from rich.console import Console

from api_toolkit.core.http_client import HttpClient
from api_toolkit.display.formatters import (
    ResponseFormatter,
    print_error,
    print_info,
)

console = Console()


@click.group(name="request")
def request_group() -> None:
    """Hacer requests HTTP a APIs"""
    pass


@request_group.command(name="get")
@click.argument("url")
@click.option(
    "--header", "-H",
    multiple=True,
    help="Header HTTP (formato: 'Key: Value'). Puedes usar múltiples veces."
)
@click.option(
    "--timeout", "-t",
    default=30,
    type=int,
    help="Timeout en segundos (default: 30)"
)
@click.option(
    "--no-headers",
    is_flag=True,
    help="No mostrar headers de respuesta"
)
def get_command(
    url: str,
    header: tuple[str, ...],
    timeout: int,
    no_headers: bool,
) -> None:
    """
    Hacer GET request a una URL
    
    Ejemplo:
        api-toolkit request get https://api.github.com/users/octocat
        
        api-toolkit request get https://api.example.com/users \\
            -H "Authorization: Bearer token123" \\
            -H "Accept: application/json"
    """
    headers = _parse_headers(header)
    
    with console.status("[bold green]Making request..."):
        try:
            client = HttpClient(timeout=timeout)
            response = client.get(url, headers=headers)
            
            console.clear_live()
            print_info(f"Request completed in {response.elapsed_time * 1000:.0f}ms")
            ResponseFormatter.format_response(response, show_headers=not no_headers)
            
        except httpx.HTTPError as e:
            console.clear_live()
            print_error(str(e))
            raise click.Abort()


@request_group.command(name="post")
@click.argument("url")
@click.option(
    "--header", "-H",
    multiple=True,
    help="Header HTTP (formato: 'Key: Value')"
)
@click.option(
    "--data", "-d",
    help="Body del request (JSON string o plain text)"
)
@click.option(
    "--timeout", "-t",
    default=30,
    type=int,
    help="Timeout en segundos"
)
@click.option(
    "--no-headers",
    is_flag=True,
    help="No mostrar headers de respuesta"
)
def post_command(
    url: str,
    header: tuple[str, ...],
    data: Optional[str],
    timeout: int,
    no_headers: bool,
) -> None:
    """
    Hacer POST request a una URL
    
    Ejemplo:
        api-toolkit request post https://api.example.com/users \\
            -H "Content-Type: application/json" \\
            -d '{"name": "John Doe", "email": "john@example.com"}'
    """
    headers = _parse_headers(header)
    
    with console.status("[bold green]Making request..."):
        try:
            client = HttpClient(timeout=timeout)
            response = client.post(url, headers=headers, body=data)
            
            console.clear_live()
            print_info(f"Request completed in {response.elapsed_time * 1000:.0f}ms")
            ResponseFormatter.format_response(response, show_headers=not no_headers)
            
        except httpx.HTTPError as e:
            console.clear_live()
            print_error(str(e))
            raise click.Abort()


@request_group.command(name="put")
@click.argument("url")
@click.option("--header", "-H", multiple=True, help="Header HTTP")
@click.option("--data", "-d", help="Body del request")
@click.option("--timeout", "-t", default=30, type=int)
@click.option("--no-headers", is_flag=True)
def put_command(
    url: str,
    header: tuple[str, ...],
    data: Optional[str],
    timeout: int,
    no_headers: bool,
) -> None:
    """Hacer PUT request a una URL"""
    headers = _parse_headers(header)
    
    with console.status("[bold green]Making request..."):
        try:
            client = HttpClient(timeout=timeout)
            response = client.put(url, headers=headers, body=data)
            
            console.clear_live()
            print_info(f"Request completed in {response.elapsed_time * 1000:.0f}ms")
            ResponseFormatter.format_response(response, show_headers=not no_headers)
            
        except httpx.HTTPError as e:
            console.clear_live()
            print_error(str(e))
            raise click.Abort()


@request_group.command(name="delete")
@click.argument("url")
@click.option("--header", "-H", multiple=True, help="Header HTTP")
@click.option("--timeout", "-t", default=30, type=int)
@click.option("--no-headers", is_flag=True)
def delete_command(
    url: str,
    header: tuple[str, ...],
    timeout: int,
    no_headers: bool,
) -> None:
    """Hacer DELETE request a una URL"""
    headers = _parse_headers(header)
    
    with console.status("[bold green]Making request..."):
        try:
            client = HttpClient(timeout=timeout)
            response = client.delete(url, headers=headers)
            
            console.clear_live()
            print_info(f"Request completed in {response.elapsed_time * 1000:.0f}ms")
            ResponseFormatter.format_response(response, show_headers=not no_headers)
            
        except httpx.HTTPError as e:
            console.clear_live()
            print_error(str(e))
            raise click.Abort()


def _parse_headers(headers: tuple[str, ...]) -> dict[str, str]:
    """
    Parse headers desde formato CLI a dict
    
    Args:
        headers: Tupla de strings en formato "Key: Value"
        
    Returns:
        Dict con headers parseados
    """
    parsed = {}
    for header in headers:
        if ":" not in header:
            print_error(f"Header inválido: '{header}'. Formato esperado: 'Key: Value'")
            raise click.Abort()
        
        key, value = header.split(":", 1)
        parsed[key.strip()] = value.strip()
    
    return parsed