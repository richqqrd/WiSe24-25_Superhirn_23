import logging
from typing import Dict, Any, Optional

import requests


class HttpClient:
    def __init__(self, base_url: str):
        """
        Initialize the HttpClient with the base URL.

        Args:
            base_url (str): The base URL for the HTTP client.
        """
        self.base_url = base_url
        self.session = requests.Session()

    def post(self, endpoint: str, data: Dict[str, Any], timeout: int = 10) -> Optional[Dict[str, Any]]:
        """
        Send a POST request to the specified endpoint with the given data.

        Args:
            endpoint (str): The endpoint to send the POST request to.
            data (Dict[str, Any]): The JSON data to include in the POST request.
            timeout (int, optional): The timeout for the request in seconds.
            Defaults to 10.

        Returns:
            Optional[Dict[str, Any]]: The JSON response from the server,
            if the request is successful.

        Raises:
            requests.exceptions.Timeout: If the request times out.
            requests.exceptions.RequestException: If the request fails.
        """
        try:
            response = self.session.post(
                f"{self.base_url}/{endpoint}",
                headers={'Content-Type': 'application/json'},
                json=data,
                timeout=timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            logging.error("Request timed out.")
            raise
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")
            raise
