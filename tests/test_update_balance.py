import unittest
import json
from unittest.mock import patch, mock_open

from update_balance import main


class TestUpdateBalance(unittest.TestCase):
    @patch("update_balance.requests.get")
    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data=json.dumps({"up": {"token": "test_token", "account_id": "test_account_id"}}),
    )
    def test_main(self, mock_file, mock_get):
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {"attributes": {"balance": {"value": "100.00"}}}}

        import sys
        sys.argv = ["update_balance.py"]
        main()

        self.assertEqual(mock_file.call_count, 2)
        mock_get.assert_called_once_with(
            "https://api.up.com.au/api/v1/accounts/test_account_id",
            headers={"Authorization": "Bearer test_token"},
        )


if __name__ == "__main__":
    unittest.main()
