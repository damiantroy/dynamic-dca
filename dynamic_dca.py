import argparse
import json
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def get_config():
    """
    Read the configuration file.
    """
    risk_data = read_json_file("data/risk.json")
    balance_data = read_json_file("data/balance.json")
    config_data = read_json_file("config/config.json")
    balance = balance_data["balance"]
    return risk_data, balance, config_data


def calculate_buy_amount(asset_config, risk, balance):
    """
    Calculate the amount to buy based on the asset configuration, risk and balance.

    Parameters:
    asset_config (dict): The configuration for the asset.
    risk (float): The risk associated with the asset.
    balance (float): The current balance.

    Returns:
    int: The amount to buy.
    """
    buy_base = asset_config["buy_base"]
    buy_risk_min = asset_config["buy_risk_min"]
    buy_risk_max = asset_config["buy_risk_max"]
    buy_min_percent = asset_config["buy_min_percent"]
    buy_max_percent = asset_config["buy_max_percent"]

    risk_range = buy_risk_max - buy_risk_min
    risk_difference = buy_risk_max - risk
    risk_proportion = risk_difference / risk_range
    buy_percentage = (risk_proportion * (buy_max_percent - buy_min_percent)) + buy_min_percent
    buy_amount = buy_base + balance * (buy_percentage / 100)
    return int(buy_amount)


def calculate_sell_percent(asset_config, risk):
    """
    Calculate the percentage to sell based on the asset configuration and risk.

    Parameters:
    asset_config (dict): The configuration for the asset.
    risk (float): The risk associated with the asset.

    Returns:
    float: The percentage to sell.
    """
    sell_risk_min = asset_config["sell_risk_min"]
    sell_risk_max = asset_config["sell_risk_max"]
    sell_min_percent = asset_config["sell_min_percent"]
    sell_max_percent = asset_config["sell_max_percent"]

    risk_range = sell_risk_max - sell_risk_min
    risk_difference = risk - sell_risk_min
    risk_proportion = risk_difference / risk_range
    sell_percentage = (risk_proportion * (sell_max_percent - sell_min_percent)) + sell_min_percent
    return round(sell_percentage, 2)


def read_json_file(file_path):
    """
    Read a JSON file and return its content.

    Parameters:
    file_path (str): The path to the JSON file.

    Returns:
    dict: The content of the JSON file.
    """
    with open(file_path, "r") as f:
        return json.load(f)


def show_output(output):
    """
    Show the output in a user-friendly way.

    Parameters:
    output (list): The output to display.
    """
    for message in output:
        print(message)


def send_email(output, email_config):
    """
    Send an email with the output.

    Parameters:
    output (list): The output to send.
    email_config (dict): The email configuration.
    """
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    logging.info("Sending email...")
    msg = MIMEMultipart()
    msg["From"] = email_config["from"]
    msg["To"] = email_config["to"]
    msg["Subject"] = email_config["subject"]
    msg.attach(MIMEText("\n".join(output), "plain"))

    server = smtplib.SMTP(email_config["smtp_server"], email_config["smtp_port"])
    server.send_message(msg)
    server.quit()


def calculate_buy_and_sell_amounts(risk_data, balance, config):
    """
    Main function to calculate buy and sell amounts for each asset based on their risk and configuration.
    """
    output = []

    for asset, asset_config in config["asset"].items():
        risk = risk_data[asset]["risk"]
        if asset_config["buy_risk_min"] <= risk <= asset_config["buy_risk_max"]:
            buy_amount = calculate_buy_amount(asset_config, risk, balance)
            output.append(
                f"Buy ${buy_amount} {asset}, risk {risk} \u2208 ({asset_config['buy_risk_min']},"
                f"{asset_config['buy_risk_max']})."
            )
        elif asset_config["sell_risk_min"] <= risk <= asset_config["sell_risk_max"]:
            starting_coins = asset_config["starting_coins"]
            sell_percent = calculate_sell_percent(asset_config, risk)
            decimal_places = len(str(starting_coins).split(".")[1])
            sell_coins = round(starting_coins * (sell_percent / 100), decimal_places)
            remaining_coins = round(starting_coins - sell_coins, decimal_places)
            output.append(
                f"Sell {sell_percent}% ({sell_coins}) {asset} (cumulatively),"
                f" leaving {remaining_coins} {asset},"
                f" risk {risk} \u2208 ({asset_config['sell_risk_min']},{asset_config['sell_risk_max']})."
            )
        else:
            output.append(
                f"Hold {asset}, risk {risk} \u2209"
                f" ({asset_config['buy_risk_min']},{asset_config['buy_risk_max']}) \u222A"
                f" ({asset_config['sell_risk_min']},{asset_config['sell_risk_max']})."
            )
    return output


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send email using Postfix")
    parser.add_argument("-e", "--email", help="Send email", action="store_true")
    args = parser.parse_args()
    risk_data, balance, config = get_config()
    output_data = calculate_buy_and_sell_amounts(risk_data, balance, config)
    if args.email:
        send_email(output_data, config["email"])
    else:
        show_output(output_data)
