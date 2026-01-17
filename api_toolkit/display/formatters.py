"""
Formatters para mostrar información en terminal con Rich
"""
import json
from typing import Optional

from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table

from api_toolkit.models.request_model import HttpResponse

console = Console()


class ResponseFormatter:
    """Formatea responses HTTP para display en terminal"""
    
    @staticmethod
    def format_response(response: HttpResponse, show_headers: bool = True) -> None:
        """
        Muestra una respuesta HTTP formateada
        
        Args:
            response: HttpResponse a mostrar
            show_headers: Si mostrar los headers de la respuesta
        """
        # Status y métricas
        status_color = ResponseFormatter._get_status_color(response.status_code)
        
        console.print()
        console.print(Panel(
            f"[{status_color}]Status:[/{status_color}] {response.status_code} "
            f"{ResponseFormatter._get_status_text(response.status_code)}\n"
            f"[cyan]Time:[/cyan] {response.elapsed_time * 1000:.0f}ms\n"
            f"[cyan]Size:[/cyan] {len(response.body)} bytes",
            title=f"[bold]Response - {response.request.method} {response.request.url}[/bold]",
            border_style=status_color,
        ))
        
        # Headers
        if show_headers and response.headers:
            console.print("\n[bold]Headers:[/bold]")
            headers_table = Table(show_header=False, box=None, padding=(0, 2))
            headers_table.add_column(style="cyan")
            headers_table.add_column()
            
            for key, value in response.headers.items():
                # Mostrar solo algunos headers importantes
                if key.lower() in [
                    "content-type", "content-length", "server",
                    "date", "cache-control", "x-ratelimit-remaining"
                ]:
                    headers_table.add_row(key, value)
            
            console.print(headers_table)
        
        # Body
        console.print("\n[bold]Body:[/bold]")
        ResponseFormatter._format_body(response)
        console.print()
    
    @staticmethod
    def _format_body(response: HttpResponse) -> None:
        """Formatea el body según el content-type"""
        content_type = response.headers.get("content-type", "")
        
        # JSON
        if "application/json" in content_type:
            try:
                parsed = json.loads(response.body)
                formatted = json.dumps(parsed, indent=2, ensure_ascii=False)
                syntax = Syntax(formatted, "json", theme="monokai", line_numbers=False)
                console.print(syntax)
            except json.JSONDecodeError:
                console.print(response.body)
        
        # HTML
        elif "text/html" in content_type:
            # Mostrar solo primeras líneas de HTML
            lines = response.body.split("\n")[:10]
            preview = "\n".join(lines)
            if len(lines) >= 10:
                preview += "\n..."
            syntax = Syntax(preview, "html", theme="monokai", line_numbers=False)
            console.print(syntax)
            console.print(f"[dim](HTML response truncated, {len(response.body)} bytes total)[/dim]")
        
        # XML
        elif "application/xml" in content_type or "text/xml" in content_type:
            syntax = Syntax(response.body[:500], "xml", theme="monokai", line_numbers=False)
            console.print(syntax)
            if len(response.body) > 500:
                console.print(f"[dim](XML truncated, {len(response.body)} bytes total)[/dim]")
        
        # Plain text
        else:
            # Limitar output de texto plano
            if len(response.body) > 1000:
                console.print(response.body[:1000])
                console.print(f"[dim]... ({len(response.body)} bytes total)[/dim]")
            else:
                console.print(response.body)
    
    @staticmethod
    def _get_status_color(status_code: int) -> str:
        """Retorna color según status code"""
        if 200 <= status_code < 300:
            return "green"
        elif 300 <= status_code < 400:
            return "yellow"
        elif 400 <= status_code < 500:
            return "orange1"
        elif 500 <= status_code < 600:
            return "red"
        else:
            return "white"
    
    @staticmethod
    def _get_status_text(status_code: int) -> str:
        """Retorna texto descriptivo del status code"""
        status_texts = {
            200: "OK",
            201: "Created",
            204: "No Content",
            301: "Moved Permanently",
            302: "Found",
            400: "Bad Request",
            401: "Unauthorized",
            403: "Forbidden",
            404: "Not Found",
            405: "Method Not Allowed",
            500: "Internal Server Error",
            502: "Bad Gateway",
            503: "Service Unavailable",
        }
        return status_texts.get(status_code, "")


def print_error(message: str) -> None:
    """Muestra un mensaje de error"""
    console.print(f"[bold red]✗ Error:[/bold red] {message}")


def print_success(message: str) -> None:
    """Muestra un mensaje de éxito"""
    console.print(f"[bold green]✓[/bold green] {message}")


def print_info(message: str) -> None:
    """Muestra un mensaje informativo"""
    console.print(f"[cyan]ℹ[/cyan] {message}")