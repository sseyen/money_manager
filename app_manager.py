from transaction_manager import TransactionManager
from datetime import datetime

class AppManager:
    def __init__(self):
        """
        Initializes the app manager.
        """
        self.transaction_manager = TransactionManager()
        
    def menu(self):
        """
        Displays the main menu and handles user input.
        """
        while True:
            print("\n--- Menu ---")
            print("1. Add transaction")
            print("2. Delete transaction")
            print("3. Update transaction")
            print("4. List transactions by date")
            print("5. Visualize monthly expenses")
            print("6. Visualize expenses for a specific month")
            print("7. Exit")

            choice = input("Choose an action: ")

            if choice == "1":
                self.add_transaction()
            elif choice == "2":
                self.delete_transaction()
            elif choice == "3":
                self.update_transaction()
            elif choice == "4":
                self.list_transactions_by_date()
            elif choice == "5":
                self.transaction_manager.visualize_monthly_expenses()
            elif choice == "6":
                self.visualize_expenses_for_month()
            elif choice == "7":
                break
            else:
                print("Invalid choice. Please try again.")
                
    def add_transaction(self):
        """
        Adds a new transaction.
        """
        date = self.get_valid_date("Enter date (YYYY-MM-DD): ")
        amount = self.get_valid_float("Enter amount: ")
        category = input("Enter category: ")
        description = input("Enter description: ")
        self.transaction_manager.add_transaction(date, amount, category, description)
        
    def delete_transaction(self):
        """
        Deletes a transaction with the given id.
        """
        id = self.get_valid_int("Enter transaction ID to delete: ")
        self.transaction_manager.delete_transaction(id)
        
    def update_transaction(self):
        """
        Updates a transaction with the given id.
        """
        id = self.get_valid_int("Enter transaction ID to update: ")

        # Input for updating the date
        date = input("Enter new date (YYYY-MM-DD) or press Enter to skip: ")
        if date:
            if not self.validate_date_format(date):
                print("Invalid date format. Skipping update of the date.")
                date = None

        # Input for updating the amount
        amount = input("Enter new amount or press Enter to skip: ")
        if amount:
            try:
                amount = float(amount)
            except ValueError:
                print("Invalid amount entered. Skipping update of the amount.")
                amount = None

        # Input for updating the category
        category = input("Enter new category or press Enter to skip: ")

        # Input for updating the description
        description = input("Enter new description or press Enter to skip: ")

        # Update the transaction
        self.transaction_manager.update_transaction(
            id,
            date if date else None,
            amount if amount else None,
            category if category else None,
            description if description else None
        )
        
    def list_transactions_by_date(self):
        """
        Lists transactions by date.
        """
        start_date = input("Enter start date (YYYY, YYYY-MM or YYYY-MM-DD) or leave empty to list all: ")
        end_date = input("Enter end date (YYYY, YYYY-MM or YYYY-MM-DD) or leave empty: ")

        self.transaction_manager.list_transactions_by_date(start_date, end_date)
                
    def visualize_expenses_for_month(self):
        """
        Visualizes expenses for a specific month.
        """
        year = int(input("Enter year (YYYY): "))
        month = int(input("Enter month (1-12): "))
        self.transaction_manager.visualize_expenses_for_month(year, month)
        
    def get_valid_date(self, prompt: str) -> datetime:
        """
        Gets a valid date from the user.
        """
        while True:
            date_str = input(prompt)
            try:
                datetime.strptime(date_str, "%Y-%m-%d")
                return date_str
            except ValueError:
                print("Invalid date format. Please enter the date in YYYY-MM-DD format.")

    def get_valid_int(self, prompt: str) -> int:
        """
        Gets a valid integer from the user.
        """
        while True:
            try:
                return int(input(prompt))
            except ValueError:
                print("Invalid input. Please enter a valid integer.")

    def get_valid_float(self, prompt: str) -> float:
        """
        Gets a valid float from the user.
        """
        while True:
            try:
                return float(input(prompt))
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    def validate_date_format(self, date_str: str) -> bool:
        """
        Validates the date format.
        """
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            return False
