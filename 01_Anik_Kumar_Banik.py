import csv
import pandas as pd
from datetime import datetime

class PersonalFinanceManager:
    def __init__(self, filename='finance_data.csv'):
        self.filename = filename
        self.init_file()

    def init_file(self):
        
        try:
            with open(self.filename, 'x', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Date', 'Category', 'Type', 'Amount'])
        except FileExistsError:
            pass

    def add_transaction(self, category, trans_type, amount):
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(self.filename, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([date, category, trans_type, amount])
        print(f"Transaction added: {trans_type} of {amount} in {category}.")

    def view_transactions(self):
        print("Date\t\t\tCategory\tType\tAmount")
        with open(self.filename, 'r') as file:
            reader = csv.reader(file)
            next(reader)  
            for row in reader:
                print('\t'.join(row))

    def calculate_total(self, trans_type):
        total = 0
        with open(self.filename, 'r') as file:
            reader = csv.reader(file)
            next(reader)  
            for row in reader:
                if row[2].lower() == trans_type.lower():
                    total += float(row[3])
        return total

    def category_expenses(self):
        df = pd.read_csv(self.filename)
        category_sum = df[df['Type'].str.lower() == 'expense'].groupby('Category')['Amount'].sum()
        return category_sum

    def suggest_savings(self):
        total_income = self.calculate_total('Income')
        total_expenses = self.calculate_total('Expense')
        if total_income > total_expenses:
            savings = total_income - total_expenses
            suggestion = f"You have a net saving of {savings}. Consider investing it."
        else:
            suggestion = "Your expenses exceed your income. Consider reviewing your expenses to find savings opportunities."
        return suggestion

    def show_summary(self):
        income = self.calculate_total('Income')
        expenses = self.calculate_total('Expense')
        print(f"\nSummary:\nTotal Income: {income}\nTotal Expenses: {expenses}\nNet Savings: {income - expenses}\n")
        print("Expenses by Category:")
        print(self.category_expenses())
        print("\nSavings Suggestion:")
        print(self.suggest_savings())


manager = PersonalFinanceManager()


while True:
    category = input("Enter transaction category: ")
    trans_type = input("Enter transaction type (Income/Expense): ")
    amount = float(input("Enter transaction amount: "))
    manager.add_transaction(category, trans_type, amount)

    more = input("Do you want to add another transaction? (yes/no): ").strip().lower()
    if more != 'yes':
        break


print("\nAll Transactions:")
manager.view_transactions()


manager.show_summary()
