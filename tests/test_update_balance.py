from unittest.mock import MagicMock, mock_open, patch

from dynamic_dca.update_balance import load_provider, main


def test_load_provider():
    BankProviderClass = load_provider("providers.banks.up_bank.UpBank")
    bank_provider = BankProviderClass()
    assert bank_provider.get_balance() is not None


@patch("json.dump")
@patch(
    "builtins.open",
    new_callable=mock_open,
    read_data='{"provider": {"bank": "providers.banks.up_bank.UpBank"}}',
)
@patch("dynamic_dca.update_balance.load_provider")
def test_main(mock_load_provider, mock_file, mock_json_dump):
    mock_provider = MagicMock()
    mock_provider.get_balance.return_value = 1000.0
    mock_load_provider.return_value.return_value = mock_provider
    mock_file.return_value.name = "data/bank.json"

    main()

    mock_provider.get_balance.assert_called_once()
    mock_json_dump.assert_called_once()
    args, _ = mock_json_dump.call_args
    assert args[0] == {"balance": 1000.0}
