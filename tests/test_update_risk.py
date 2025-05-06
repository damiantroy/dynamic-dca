import unittest
from unittest.mock import patch, mock_open, call
import json
from dynamic_dca.update_risk import main


def get_read_data():
    return {
        "config/secrets.json": json.dumps(
            {
                "alphasquared": "AbCdEfG...",
                "up": {
                    "token": "up:yeah:AbCdEfG...",
                    "account_id": "99999999-1111-2222-3333-abcdefabcdef",
                },
            }
        ),
        "data/risk.json": json.dumps(
            {
                "BTC": {"risk": 50, "updated": 1717014602.7140715},
                "ETH": {"risk": 50, "updated": 1717014605.4223795},
            }
        ),
    }


class TestUpdateRisks(unittest.TestCase):
    @patch("dynamic_dca.update_risk.requests.get")
    @patch("builtins.open", new_callable=mock_open)
    def test_main(self, mock_file, mock_get):
        read_data = get_read_data()

        def mocked_open(file, mode="r", *args, **kwargs):
            if file in read_data and "r" in mode:
                return mock_open(read_data=read_data[file]).return_value
            elif "w" in mode:
                return mock_open().return_value
            else:
                raise FileNotFoundError(f"No such file: '{file}'")

        mock_file.side_effect = mocked_open

        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {"current_risk": 50}

        main()

        self.assertEqual(mock_file.call_count, 3)
        expected_calls = [
            call(
                "https://alphasquared.io/wp-json/as/v1/asset-info?symbol=BTC",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": "AbCdEfG...",
                    "User-Agent": "Mozilla/5.0",
                },
            ),
            call(
                "https://alphasquared.io/wp-json/as/v1/asset-info?symbol=ETH",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": "AbCdEfG...",
                    "User-Agent": "Mozilla/5.0",
                },
            ),
        ]
        mock_get.assert_has_calls(expected_calls, any_order=True)
        self.assertEqual(mock_get.call_count, 2)


if __name__ == "__main__":
    unittest.main()
