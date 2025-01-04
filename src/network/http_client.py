"""Module for handling HTTP client functionality."""

import logging
from typing import Dict, Any, Optional

import requests


class HttpClient:
    """HTTP client for making requests to the game server.

    This class handles making HTTP requests to the game server with proper
    error handling and logging.

    Attributes:
        base_url: Base URL for the HTTP requests
        session: Requests session for connection pooling
    """

    def __init__(self: "HttpClient", base_url: str) -> None:
        """Initialize the HttpClient.

        Args:
            base_url: The base URL for the HTTP client
        """
        self.base_url = base_url
        self.session = requests.Session()

    def post(
        self: "HttpClient", endpoint: str, data: Dict[str, Any], timeout: int = 10
    ) -> Optional[Dict[str, Any]]:
        """Send a POST request to the specified endpoint.

        Args:
            endpoint: The endpoint to send the POST request to
            data: The JSON data to include in the POST request
            timeout: The timeout for the request in seconds, defaults to 10

        Returns:
            The JSON response from the server if successful

        Raises:
            requests.exceptions.Timeout: If the request times out
            requests.exceptions.RequestException: If the request fails
        """
        try:
            response = self.session.post(
                f"{self.base_url}/{endpoint}",
                headers={"Content-Type": "application/json"},
                json=data,
                timeout=timeout,
            )
            response.raise_for_status()
            return response.json()
             
        except requests.exceptions.HTTPError as e:
            logging.error(f"HTTP Error: {e.response.status_code} - {e.response.reason}")
            if e.response.status_code == 404:
                return {"error": "Server nicht gefunden"}
            elif e.response.status_code == 500:
                return {"error": "Interner Server-Fehler"}
            elif e.response.status_code == 408:
                return {"error": "Zeitüberschreitung"}
            return {"error": f"HTTP Fehler: {e.response.status_code}"}
            
        except requests.exceptions.ConnectionError:
            logging.error("Verbindung zum Server fehlgeschlagen")
            return {"error": "Verbindung fehlgeschlagen"}
            
        except requests.exceptions.Timeout:
            logging.error("Zeitüberschreitung bei Server-Anfrage")
            return {"error": "Zeitüberschreitung"}
            
        except Exception as e:
            logging.error(f"Unerwarteter Fehler: {str(e)}")
            return {"error": "Unerwarteter Fehler"}
