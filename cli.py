import click
from transaction_manager import TransactionManager
from datetime import datetime

manager = TransactionManager()

@click.group()
def cli():
    """CLI for managing transactions."""
    pass

@cli.command()
@click.argument("date")
@click.argument("amount", type=float)
@click.argument("category")
@click.argument("description")
def add(date, amount, category, description):
    """
    Adds a new transaction.
    """
    try:
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        manager.add_transaction(date_obj, amount, category, description)
        print(f"Transaction on {date} added successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
        
@cli.command()
@click.argument("transaction_id", type=int)
def delete(transaction_id):
    """
    Deletes a transaction with the given id.
    """
    try:
        manager.delete_transaction(transaction_id)
        print(f"Transaction with ID {transaction_id} deleted successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
        
@cli.command()
@click.argument("transaction_id", type=int)
@click.argument("date", required=False)
@click.argument("amount", type=float, required=False)
@click.argument("category", required=False)
@click.argument("description", required=False)
def update(transaction_id, date, amount, category, description):
    """
    Updates a transaction with the given id.
    """
    try:
        manager.update_transaction(transaction_id, date, amount, category, description)
    except Exception as e:
        print(f"An error occurred: {e}")
        
@cli.command()
@click.argument("start-date", required=False)
@click.argument("end-date", required=False)
def list(start_date, end_date):
    """
    Lists transactions by date if dates are provided, otherwise lists all transactions.
    """
    try:
        manager.list_transactions_by_date(start_date, end_date)
    except Exception as e:
        print(f"An error occurred while listing transactions: {e}")
        
@cli.command()
@click.argument("date", required=False)
def graph(date):
    """
    Displays a graph of transactions for the specified year and month.
    """
    try:
        if date:
            year, month = date.split("-")
            manager.visualize_expenses_for_month(int(year), int(month))
        else:
            manager.visualize_monthly_expenses()
    except Exception as e:
        print(f"An error occurred: {e}")
    
if __name__ == "__main__":
    cli()
