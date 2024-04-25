import json
import time
import requests
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

cache_time = 10 * 60  # 10 minutes
risk_urls = {
    "BTC": {
        "URL": "https://alphasquared.io/wp-json/as/v1/latest-risk-value",
        "return": "latest_risk_value",
    },
    "ETH": {
        "URL": "https://alphasquared.io/wp-json/as/v1/latest-risk-value_ETH",
        "return": "latest_risk_value_ETH",
    },
}


def main():
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
    for asset, config in risk_urls.items():
        if asset in risk and risk[asset]["updated"] > time.time() - cache_time:
            logging.info(f"Risk for {asset} is up-to-date")
            continue
        logging.debug(f"Getting risk for {asset} ({config['URL']})...")
        response = requests.get(
            config["URL"],
            headers={
                "Content-Type": "application/json",
                "Authorization": secrets["alphasquared"],
            },
        )
        if response.status_code == 200:
            logging.info(f"Risk for {asset}: {response.json()[config['return']]}")
            risk[asset] = {
                "risk": float(response.json()[config["return"]]),
                "updated": time.time(),
            }
            risks_updated = True
        else:
            logging.error(f"Error getting risk for {asset}: {response.status_code}")

    # Write the risk scores to a file
    if risks_updated:
        logging.debug("Writing risk scores to file...")
        with open("data/risk.json", "w") as f:
            json.dump(risk, f, indent=2)


if __name__ == "__main__":
    main()
