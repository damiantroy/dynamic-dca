# dynamic-dca
Calculate a dynamic DCA buy/sell based on a risk index. It currently has a very specific use case, the risk
index is from AlphaSquare, and the bank is an Australian bank named Up.

## Config
Create config files based on the examples in the `config` directory, and edit them. You should have the
following config files:
* `config/config.json`
* `config/secrets.json`

## Usage

Environment setup:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Update your bank balance:

```bash
python update_balance.py
```

Update the risk values:

```bash
python update_risks.py
```

Display the dynamic DCA action to take based on your config:

```bash
python dynamic_dca.py
```
