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
        except requests.exceptions.Timeout:
            logging.error("Request timed out.")
            raise
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")
            raise
