import sys
import os
from unittest.mock import patch, mock_open

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from transaction_manager import TransactionManager


@patch("transaction_manager.open", new_callable=mock_open)
@patch("transaction_manager.json.dump")
@patch("transaction_manager.json.load", return_value=[])
def test_add_transaction(mock_json_load, mock_json_dump, mock_file):
    """
    Test adding a transaction with file operations mocked.
    """
    
    manager = TransactionManager()

    manager.add_transaction("2023-09-14", -100, "groceries", "Supermarket shopping")

    assert len(manager.transactions) == 1
    assert manager.transactions[0].amount == -100
    assert manager.transactions[0].category == "groceries"
    assert manager.transactions[0].description == "Supermarket shopping"

@patch("transaction_manager.open", new_callable=mock_open)
@patch("transaction_manager.json.dump")
@patch("transaction_manager.json.load", return_value=[])
def test_delete_transaction(mock_json_load, mock_json_dump, mock_file):
    """
    Test deleting a transaction with file operations mocked.
    """
    
    manager = TransactionManager()

    manager.add_transaction("2023-09-14", -100, "groceries", "Supermarket shopping")

    manager.delete_transaction(1)

    assert len(manager.transactions) == 0

@patch("transaction_manager.open", new_callable=mock_open)
@patch("transaction_manager.json.dump")
@patch("transaction_manager.json.load", return_value=[])
def test_update_transaction(mock_json_load, mock_json_dump, mock_file):
    """
    Test updating a transaction with file operations mocked.
    """
    
    manager = TransactionManager()

    manager.add_transaction("2023-09-14", -100, "groceries", "Supermarket shopping")
    
    manager.update_transaction(1, amount=-200, description="Updated shopping")

    assert manager.transactions[0].amount == -200
    assert manager.transactions[0].description == "Updated shopping"
    