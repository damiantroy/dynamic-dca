from unittest.mock import MagicMock, mock_open, patch

from dynamic_dca.update_risk import load_provider, main


@patch("requests.get")
@patch(
    "builtins.open",
    new_callable=mock_open,
    read_data='{"risks":{"alphasquared":"key"}}',
)
@patch("json.dump")
@patch(
    "builtins.open",
    new_callable=mock_open,
    read_data='{"BTC": {"risk": 20.0,"updated":0.0}}',
)
def test_load_provider(mock_file, mock_json_dump, mock_secrets, mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {"current_risk": 20.0}
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    RiskProviderClass = load_provider("providers.risks.alphasquared.AlphaSquared")
    risk_provider = RiskProviderClass()

    assert risk_provider.get_risk() is not None
    assert risk_provider.get_risk()["BTC"]["risk"] == 20.0


@patch("json.dump")
@patch(
    "builtins.open",
    new_callable=mock_open,
    read_data='{"provider": {"risk": "providers.risks.alphasquared.AlphaSquared"}}',
)
@patch("dynamic_dca.update_risk.load_provider")
def test_main(mock_load_provider, mock_file, mock_json_dump):
    mock_provider = MagicMock()
    mock_provider.get_risk.return_value = 80.0
    mock_load_provider.return_value.return_value = mock_provider
    mock_file.return_value.name = "data/bank.json"

    main()

    mock_provider.get_risk.assert_called_once()
    mock_json_dump.assert_called_once()
    args, _ = mock_json_dump.call_args
    assert args[0] == 80.0
