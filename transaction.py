from datetime import datetime

class Transaction:
    def __init__(self,  id, date, amount, category, description):
        """
        Initializes the transaction.
        """
        self.id = id
        self.date = datetime.strptime(date, "%Y-%m-%d")
        self.amount = amount
        self.category = category
        self.description = description

    def __str__(self):
        """
        Returns a string representation of the transaction.
        """
        return f"ID: {self.id}\nDate: {self.date}\nAmount: {self.amount}\nCategory: {self.category}\nDescription: {self.description}"
