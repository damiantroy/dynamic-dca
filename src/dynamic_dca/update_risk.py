#!/usr/bin/env -S uv run --script
import importlib
import json
import logging
import argparse


def load_provider(path):
    module_name, class_name = path.rsplit(".", 1)
    module = importlib.import_module(module_name)
    return getattr(module, class_name)



def main():
    parser = argparse.ArgumentParser(description="Update bank balance from Up")
    parser.add_argument("-v", "--verbose", help="Increase verbosity", action="count", default=0)
    args = parser.parse_args()

    if args.verbose == 0:
        logging.basicConfig(level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")
    elif args.verbose == 1:
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    elif args.verbose >= 2:
        logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

    with open("config/config.json") as f:
        config = json.load(f)
    RiskProviderClass = load_provider(config["provider"]["risk"])
    risk_provider = RiskProviderClass()
    risk = risk_provider.get_risk()

    # Write the risk scores to a file
    if risk:
        logging.debug("Writing risk scores to file...")
        with open("data/risk.json", "w") as f:
            json.dump(risk, f, indent=2)


if __name__ == "__main__":
    main()
