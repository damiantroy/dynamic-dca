#!/usr/bin/env -S uv run --script
import argparse
import importlib
import json
import logging
import os
import sys

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
src_path = os.path.join(project_root, "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)


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

    # Get balance from preferred bank provider
    with open("config/config.json") as f:
        config = json.load(f)
    BankProviderClass = load_provider(config["provider"]["bank"])
    bank_provider = BankProviderClass()
    balance = bank_provider.get_balance()

    # Write the bank balance to a file
    logging.debug("Saving balance to file")
    with open("data/bank.json", "w") as f:
        json.dump({"balance": balance}, f, indent=2)


if __name__ == "__main__":
    main()
