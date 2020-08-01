"""Tests the app module using unittest"""
import unittest
import json
from app import app


OK_RESPONSE = '200 OK'
NOT_FOUND_RESPONSE = '404 NOT FOUND'


class TestApp(unittest.TestCase):
    """Test app class"""

    def setUp(self):
        """Setups the app"""
        self.app = app.test_client()

    def test_island(self):
        """Tests a country without borders
        """
        expected_response = {"name": "Trinidad and Tobago", "borders": []}
        response = self.app.get('/name/Trinidad')
        self.assertEqual(str(response.status), OK_RESPONSE)
        self.assertEqual(json.loads(response.data), expected_response)

    def test_country_with_borders_less_population(self):
        """Tests a country with borders and with a population
        less than 5000000
        """
        expected_response = {
            "name": "Costa Rica",
            "borders": [
                {
                    "name": "Nicaragua",
                    "capital": "Managua",
                    "currency_code": "OJP"
                },
                {
                    "name": "Panama",
                    "capital": "Panama City",
                    "currency_code": "PAB"
                }
            ]
        }
        response = self.app.get('/name/Costa Rica')
        self.assertEqual(str(response.status), OK_RESPONSE)
        self.assertEqual(json.loads(response.data), expected_response)

    def test_country_with_borders_more_population(self):
        """Tests a country with borders and with a population
        more than 5000000
        """
        expected_response = {
            "name": "United Arab Emirates",
            "borders": [
                {
                    "name": "Oman",
                    "capital": "Muscat",
                    "currency_code": "OMR"
                },
                {
                    "name": "Saudi Arabia",
                    "capital": "Riyadh",
                    "currency_code": "TBS"
                }
            ]
        }
        response = self.app.get('/name/United%20Arab%20Emirates')
        self.assertEqual(str(response.status), OK_RESPONSE)
        self.assertEqual(json.loads(response.data), expected_response)

    def test_country_that_not_exists(self):
        """Tests a country that not exists"""
        expected_response = {
            "status": 404,
            "message": "Not Found"
        }
        response = self.app.get('/name/Nothing')
        self.assertEqual(str(response.status), NOT_FOUND_RESPONSE)
        self.assertEqual(json.loads(response.data), expected_response)
