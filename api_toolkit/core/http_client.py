"""
Cliente HTTP usando httpx
"""
import time
from typing import Optional

import httpx
from api_toolkit.models.request_model import HttpRequest, HttpResponse


class HttpClient:
    """Cliente HTTP wrapper sobre httpx"""
    
    def __init__(self, timeout: int = 30) -> None:
        self.timeout = timeout
    
    def request(
        self,
        method: str,
        url: str,
        headers: Optional[dict[str, str]] = None,
        body: Optional[str] = None,
        timeout: Optional[int] = None,
    ) -> HttpResponse:
        """
        Realiza un request HTTP
        
        Args:
            method: Método HTTP (GET, POST, etc.)
            url: URL destino
            headers: Headers opcionales
            body: Body del request (para POST/PUT)
            timeout: Timeout en segundos
            
        Returns:
            HttpResponse con la respuesta
            
        Raises:
            httpx.HTTPError: Si hay error en el request
        """
        # Crear modelo de request
        request = HttpRequest(
            method=method,
            url=url,
            headers=headers or {},
            body=body,
            timeout=timeout or self.timeout
        )
        
        # Medir tiempo de respuesta
        start_time = time.time()
        
        try:
            with httpx.Client(timeout=request.timeout) as client:
                response = client.request(
                    method=request.method,
                    url=request.url,
                    headers=request.headers,
                    content=request.body.encode() if request.body else None,
                )
                
                elapsed_time = time.time() - start_time
                
                # Crear modelo de respuesta
                http_response = HttpResponse(
                    status_code=response.status_code,
                    headers=dict(response.headers),
                    body=response.text,
                    elapsed_time=elapsed_time,
                    request=request,
                )
                
                return http_response
                
        except httpx.TimeoutException as e:
            elapsed_time = time.time() - start_time
            raise httpx.HTTPError(f"Request timeout después de {elapsed_time:.2f}s") from e
        except httpx.ConnectError as e:
            raise httpx.HTTPError(f"No se pudo conectar a {url}") from e
    
    def get(self, url: str, **kwargs: dict) -> HttpResponse:
        """Convenience method para GET"""
        return self.request("GET", url, **kwargs)
    
    def post(self, url: str, **kwargs: dict) -> HttpResponse:
        """Convenience method para POST"""
        return self.request("POST", url, **kwargs)
    
    def put(self, url: str, **kwargs: dict) -> HttpResponse:
        """Convenience method para PUT"""
        return self.request("PUT", url, **kwargs)
    
    def delete(self, url: str, **kwargs: dict) -> HttpResponse:
        """Convenience method para DELETE"""
        return self.request("DELETE", url, **kwargs)