import json
import logging
import requests

from .base_bank import BaseBank

class UpBank(BaseBank):
    def get_balance(self):
        logging.info("Getting balance from Up Bank")

        # Read token and account ID from secrets.json
        with open("config/secrets.json") as f:
            secrets = json.load(f)
            token = secrets["banks"]["up"]["token"]
            account_id = secrets["banks"]["up"]["account_id"]

        # Get the bank balance from the Up API
        url = f"https://api.up.com.au/api/v1/accounts/{account_id}"
        headers = {"Authorization": f"Bearer {token}"}
        try:
            response = requests.get(url, headers=headers)
        except Exception as e:
            raise e

        # Return the balance
        if response.status_code == 200:
            balance = float(response.json()["data"]["attributes"]["balance"]["value"])
            logging.info(f"Returning bank balance: {balance}")
            return balance
        else:
            logging.error(f"Error getting bank balance: {response.status_code}")
            return None
