# dynamic-dca
Calculate a dynamic DCA buy/sell based on a risk index. It currently has a very specific use case,
where the risk index is from [AlphaSquared](https://alphasquared.io/), and the bank is an Australian
bank named [Up Bank](https://up.com.au/).

Pre-requisites:
* Python 3.10+
* `uv`

## Config
Create config files based on the examples in the `config` directory, and edit them. You need the
following config files:
* `config/config.json`
  * 'buy_reference' is optional.
* `config/secrets.json`

## Usage

To update your bank balance:

```bash
uv run update_balance
```

Update the risk values:

```bash
uv run update_risk
```

Display the dynamic DCA action to take based on your config:

```bash
uv run dynamic_dca
```

Or to e-mail the dynamic DCA actions:

```bash
uv run dynamic_dca -e
```

## Development

Development environment setup:

```bash
make install
source .venv/bin/activate
```

To run unit tests:

```bash
make test
```

Manually run pre-commit checks:

```bash
make validate
```
