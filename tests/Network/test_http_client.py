"""Test module for HttpClient."""

import unittest
from unittest.mock import patch, Mock
import requests
from src.network.http_client import HttpClient


class TestHttpClient(unittest.TestCase):
    """Test cases for HttpClient class."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.base_url = "http://test.com"
        self.client = HttpClient(self.base_url)
        self.test_url = "endpoint"
        self.test_data = {"key": "value"}

    def test_init(self):
        """Test initialization of HttpClient."""
        self.assertEqual(self.client.base_url, self.base_url)
        self.assertIsNotNone(self.client.session)

    @patch("requests.Session.post")
    def test_post_success(self, mock_post):
        """Test successful POST request."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"response": "success"}
        mock_post.return_value = mock_response

        response = self.client.post(self.test_url, self.test_data)

        self.assertEqual(response, {"response": "success"})
        mock_post.assert_called_once_with(
            f"{self.base_url}/endpoint",
            headers={"Content-Type": "application/json"},
            json=self.test_data,
            timeout=10
        )

    @patch("requests.Session.post")
    def test_post_http_error(self, mock_post):
        """Test POST request with HTTP error."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
            "404 Client Error"
        )
        mock_post.return_value = mock_response

        with self.assertRaises(requests.exceptions.HTTPError):
            self.client.post(self.test_url, self.test_data)

    @patch("requests.Session.post")
    def test_post_connection_error(self, mock_post):
        """Test POST request with connection error."""
        mock_post.side_effect = requests.exceptions.ConnectionError(
            "Connection refused"
        )

        with self.assertRaises(requests.exceptions.ConnectionError):
            self.client.post(self.test_url, self.test_data)

    @patch("requests.Session.post")
    def test_post_timeout_error(self, mock_post):
        """Test POST request with timeout."""
        mock_post.side_effect = requests.exceptions.Timeout("Request timed out")

        with self.assertRaises(requests.exceptions.Timeout):
            self.client.post(self.test_url, self.test_data)

    @patch("requests.Session.post")
    def test_post_invalid_json_response(self, mock_post):
        """Test POST request with invalid JSON response."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_post.return_value = mock_response

        with self.assertRaises(ValueError):
            self.client.post(self.test_url, self.test_data)

    @patch("requests.Session.post")
    def test_post_empty_response(self, mock_post):
        """Test POST request with empty response."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = None
        mock_post.return_value = mock_response

        response = self.client.post(self.test_url, self.test_data)
        self.assertIsNone(response)


if __name__ == "__main__":
    unittest.main()