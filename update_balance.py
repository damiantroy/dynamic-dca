# Description: This script updates the bank balance from Up
import json
import requests
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def main():
    # Read token and account ID from secrets.json
    with open("config/secrets.json") as f:
        secrets = json.load(f)
        token = secrets["up"]["token"]
        account_id = secrets["up"]["account_id"]

    # Get the bank balance from the Up API
    url = f"https://api.up.com.au/api/v1/accounts/{account_id}"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)

    # Write the bank balance to a file
    if response.status_code == 200:
        balance = float(response.json()["data"]["attributes"]["balance"]["value"])
        with open("data/balance.json", "w") as f:
            json.dump({"balance": balance}, f, indent=2)
        logging.info(f"Bank balance updated: {balance}")
    else:
        logging.error(f"Error getting bank balance: {response.status_code}")


if __name__ == "__main__":
    main()
