import json
import logging
import time

import requests

from .base_risk import BaseRisk

cache_time = 10 * 60  # 10 minutes
risk_assets = ["BTC", "ETH", "XRP"]
risk_url_template = "https://alphasquared.io/wp-json/as/v1/asset-info?symbol={}"
risk_return_field = "current_risk"


class AlphaSquared(BaseRisk):
    def get_risk(self):
        # Read in the secrets file
        with open("config/secrets.json") as f:
            secrets = json.load(f)

        # Read the previous risk scores if the file exists
        risks_updated = False
        try:
            with open("data/risk.json") as f:
                risk = json.load(f)
        except FileNotFoundError:
            risk = {}

        # Get the risk for each asset
        for asset in risk_assets:
            risk_url = risk_url_template.format(asset)
            if asset in risk and risk[asset]["updated"] > time.time() - cache_time:
                logging.info(f"Risk for {asset} is up-to-date")
                continue
            logging.debug(f"Getting risk for {asset} ({risk_url})...")
            response = requests.get(
                risk_url,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": secrets["risks"]["alphasquared"],
                    "User-Agent": "Mozilla/5.0",
                },
            )
            if response.status_code == 200:
                logging.info(f"Risk for {asset}: {response.json()[risk_return_field]}")
                risk[asset] = {
                    "risk": float(response.json()[risk_return_field]),
                    "updated": time.time(),
                }
                risks_updated = True
            else:
                logging.error(f"Error getting risk for {asset}: {response.status_code}: {response.text}")

        if risks_updated:
            return risk
        else:
            return None
