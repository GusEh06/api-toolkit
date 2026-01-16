"""
Modelos de datos para requests HTTP
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class HttpRequest:
    """Representa un request HTTP"""
    method: str
    url: str
    headers: dict[str, str] = field(default_factory=dict)
    body: Optional[str] = None
    timeout: int = 30
    
    def __post_init__(self) -> None:
        """Validaciones después de inicialización"""
        self.method = self.method.upper()
        valid_methods = ["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"]
        if self.method not in valid_methods:
            raise ValueError(f"Método inválido: {self.method}")


@dataclass
class HttpResponse:
    """Representa una respuesta HTTP"""
    status_code: int
    headers: dict[str, str]
    body: str
    elapsed_time: float  # en segundos
    request: HttpRequest
    timestamp: datetime = field(default_factory=datetime.now)
    
    @property
    def is_success(self) -> bool:
        """Verifica si el status code indica éxito (2xx)"""
        return 200 <= self.status_code < 300
    
    @property
    def is_client_error(self) -> bool:
        """Verifica si es error del cliente (4xx)"""
        return 400 <= self.status_code < 500
    
    @property
    def is_server_error(self) -> bool:
        """Verifica si es error del servidor (5xx)"""
        return 500 <= self.status_code < 600


@dataclass
class RequestHistory:
    """Representa un registro en el histórico de requests"""
    id: int
    request: HttpRequest
    response: HttpResponse
    created_at: datetime = field(default_factory=datetime.now)