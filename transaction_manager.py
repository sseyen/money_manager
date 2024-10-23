import os
import json
from datetime import datetime
import matplotlib.pyplot as plt
from transaction import Transaction

class TransactionManager:
    def __init__(self):
        """
        Loads transactions from a file.
        """
        self.transactions = self.load_transactions()
        
    def load_transactions(self):
        """
        Loads transactions from a file.
        If the file does not exist, returns an empty list.
        """
        if not os.path.exists("transactions.json"):
            return []
        
        with open("transactions.json") as file:
            data = json.load(file)
            return [Transaction(**transaction) for transaction in data]
        
    def save_transactions(self):
        """
        Sorts transactions by date and saves them to a file.
        """
        sorted_transactions = sorted(self.transactions, key=lambda t: t.date)
        
        data = [
            {
                "id": t.id,
                "date": t.date.strftime("%Y-%m-%d"),
                "amount": t.amount,
                "category": t.category,
                "description": t.description
            }
            for t in sorted_transactions
        ]
        
        with open("transactions.json", "w") as file:
            json.dump(data, file, indent=4)
        print("Trasanctions saved.")
        
    def add_transaction(self, date, amount, category, description):
        """
        Adds a new transaction to the list.
        """
        new_id = max([t.id for t in self.transactions], default=0) + 1
        new_transaction = Transaction(new_id, date, amount, category, description)
        self.transactions.append(new_transaction)
        self.save_transactions()
        print("Transaction added.")
        
    def delete_transaction(self, id):
        """
        Deletes a transaction with the given id.
        """
        self.transactions = [t for t in self.transactions if t.id != id]
        self.save_transactions()
        print("Transaction deleted.")
        
    def update_transaction(self, id, date=None, amount=None, category=None, description=None):
        """
        Updates a transaction with the given id.
        """
        for transaction in self.transactions:
            if transaction.id == id:
                # If a new value is not provided, keep the old value
                new_date = date if date else transaction.date.strftime("%Y-%m-%d")
                new_amount = amount if amount else transaction.amount
                new_category = category if category else transaction.category
                new_description = description if description else transaction.description

                self.delete_transaction(id)

                self.add_transaction(new_date, new_amount, new_category, new_description)
                print(f"Transaction with the ID {id} has been updated.")
                return

        print(f"Transaction with the ID {id} not found.")
        
    def display_transactions(self, transactions):
        """
        Displays a list of transactions.
        """
        if transactions:
            print("-" * 8)
            for transaction in transactions:
                print(transaction)
                print("-" * 8)
        else:
            print("No transactions found for the specified date(s).")
        
    def list_transactions_by_year(self, year):
        """
        Lists transactions for the specified year.
        """
        filtered_transactions = [t for t in self.transactions if t.date.year == year]
        self.display_transactions(filtered_transactions)

    def list_transactions_by_month(self, year, month):
        """
        Lists transactions for the specified month.
        """
        filtered_transactions = [
            t for t in self.transactions if t.date.year == year and t.date.month == month
        ]
        self.display_transactions(filtered_transactions)

    def list_transactions_by_day(self, year, month, day):
        """
        Lists transactions for the specified day.
        """
        specific_date = datetime(year, month, day)
        filtered_transactions = [t for t in self.transactions if t.date == specific_date]
        self.display_transactions(filtered_transactions)
        
    def list_transactions_by_range(self, start_date, end_date):
        """
        Lists transactions for the specified date range.
        """
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        filtered_transactions = [
            t for t in self.transactions if start <= t.date <= end
        ]
        self.display_transactions(filtered_transactions)

    def list_transactions_by_date(self, start_date=None, end_date=None):
        """
        Lists transactions based on the date(s) provided.
        """
        if start_date and end_date:
            if start_date < end_date:
                print("Start date cannot be greater than end date.")
                return
            self.list_transactions_by_range(start_date, end_date)
        elif start_date:
            date_parts = start_date.split("-")
            if len(date_parts) == 1:
                # Entered year
                year = int(date_parts[0])
                self.list_transactions_by_year(year)
            elif len(date_parts) == 2:
                # Entered year and month
                year, month = int(date_parts[0]), int(date_parts[1])
                self.list_transactions_by_month(year, month)
            elif len(date_parts) == 3:
                # Entered year, month, and day
                year, month, day = int(date_parts[0]), int(date_parts[1]), int(date_parts[2])
                self.list_transactions_by_day(year, month, day)
        else:
            # No date entered, display all transactions
            self.display_transactions(self.transactions)
            
    def visualize_monthly_expenses(self):
        """
        Visualizes monthly expenses.
        """
        monthly_expenses = {}
        
        for transaction in self.transactions:
            if transaction.amount < 0:
                year_month = transaction.date.strftime("%Y-%m")
                if year_month not in monthly_expenses:
                    monthly_expenses[year_month] = 0.0
                monthly_expenses[year_month] += abs(transaction.amount)

        if not monthly_expenses:
            print("No expenses to display.")
            return

        sorted_months = sorted(monthly_expenses.keys())
        expenses = [monthly_expenses[month] for month in sorted_months]

        plt.figure(figsize=(10, 6))
        plt.bar(sorted_months, expenses)
        plt.xlabel("Month")
        plt.ylabel("Expenses (in currency)")
        plt.title("Monthly Expenses Overview")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def visualize_expenses_for_month(self, year, month):
        """
        Visualizes expenses for the specified month.
        """
        if month < 1 or month > 12:
            print("Invalid month. Please enter a value between 1 and 12.")
            return
        
        monthly_expenses = {}

        for transaction in self.transactions:
            if transaction.amount < 0:
                if transaction.date.year == year and transaction.date.month == month:
                    category = transaction.category
                    if category not in monthly_expenses:
                        monthly_expenses[category] = 0.0
                    monthly_expenses[category] += abs(transaction.amount)

        if not monthly_expenses:
            print(f"No expenses found for {year}-{month:02d}.")
            return

        sorted_categories = sorted(monthly_expenses.keys())
        expenses = [monthly_expenses[category] for category in sorted_categories]

        plt.figure(figsize=(8, 6))
        plt.bar(sorted_categories, expenses)
        plt.xlabel("Category")
        plt.ylabel("Expenses (in currency)")
        plt.title(f"Expenses Breakdown for {year}-{month:02d}")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
