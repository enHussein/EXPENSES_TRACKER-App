import tkinter as tk
from tkinter import ttk
from datetime import datetime
from tkcalendar import Calendar, DateEntry
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import simpledialog
from tkinter import messagebox
import requests

class ExpensesTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("$ EXPENSES TRACKER")

        for i in range(5):
            self.root.rowconfigure(i, minsize=5, weight=1)
        for i in range(2):
            self.root.columnconfigure(i, minsize=10, weight=1)

        self.root.configure(padx=10, pady=10, bg='LightGray')

        label_font = ("Helvetica", 10)

        labels = ["Amount", "Currency", "Category", "Payment Method", "Date"]
        for i, label_text in enumerate(labels):
            label = tk.Label(self.root, text=label_text + ":", font=label_font, bg='LightGray')
            label.grid(row=i, rowspan=1, column=0, padx=10, pady=5, sticky="e")

            if label_text == "Amount":
                self.amount_input_field = tk.Entry(self.root, width=15)
                self.amount_input_field.grid(row=i, column=1, padx=10, pady=5, sticky="w")

            elif label_text == "Currency":
                self.currency_method = ["USD", "GBP", "EGP", "SAR", "AED", "gas"]
                self.currency_method_var = tk.StringVar(root)
                self.currency_method_var.set(self.currency_method[0])
                entry = ttk.Combobox(self.root, textvariable=self.currency_method_var, values=self.currency_method, state='readonly')
                entry.grid(row=i, column=1, padx=10, pady=5, sticky="w")

            elif label_text == "Category":
                self.category_method = ["savings", "life expenses", "education", "grocery", "electricity", "gas", "rental", "charity"]
                self.category_method_var = tk.StringVar(root)
                self.category_method_var.set(self.category_method[0])
                entry = ttk.Combobox(self.root, textvariable=self.category_method_var, values=self.category_method, state='readonly')
                entry.grid(row=i, column=1, padx=10, pady=5, sticky="w")

            elif label_text == "Payment Method":
                self.payment_methods = ["Cash", "Credit Card", "Paypal"]
                self.payment_method_var = tk.StringVar(root)
                self.payment_method_var.set(self.payment_methods[0])
                entry = ttk.Combobox(self.root, textvariable=self.payment_method_var, values=self.payment_methods, state='readonly')
                entry.grid(row=i, column=1, padx=10, pady=5, sticky="w")

            elif label_text == "Date":
                self.date_input_field = DateEntry(self.root, width=12)
                self.date_input_field.grid(row=i, column=1, padx=10, pady=5, sticky="w")

        get_text_button = tk.Button(self.root, text="Add Expenses", bg="gray", command=self.add_expenses)
        get_text_button.grid(row=5, column=1, padx=20, pady=10, sticky="w")

        self.result_text = tk.Text(self.root, height=5, width=40, bg="yellow")
        self.result_text.grid(row=8, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        columns = ("Amount", "Currency", "Category", "Payment Method", "Datetime")
        self.tree = ttk.Treeview(self.root, columns=columns, height=20)
        self.tree.grid(row=7, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        self.tree.heading('#0', text='Num')
        self.tree.heading('Amount', text='Amount')
        self.tree.heading('Currency', text='Currency')
        self.tree.heading('Category', text='Category')
        self.tree.heading('Payment Method', text='Payment Method')
        self.tree.heading('Datetime', text='Datetime')

        self.root.columnconfigure(0, weight=1)

        self.index = 0

    def add_expenses(self):
        expenses_details = self.get_expenses()

        if expenses_details:
            self.tree.insert('', tk.END, iid=self.index, text=str(self.index), values=expenses_details[0:])
            self.index += 1

            total_usd = 0
            for item_id in self.tree.get_children():
                amount, currency = self.tree.item(item_id, "values")[:2]
                converted_amount = self.fetch_data(amount, currency)
                total_usd += converted_amount

            total_text = f'Total in USD: {total_usd:.2f} USD\n'
            self.result_text.insert(tk.END, total_text)

    def get_expenses(self):
        try:
            amount = float(self.amount_input_field.get())
        except ValueError:
            
            messagebox.showerror("Error", "Enter a valid numeric amount as expenses")
            return 

        if amount <= 0:
            
            messagebox.showerror("Error", "Amount must be greater than 0")
            return 

        currency = self.currency_method_var.get()
        category = self.category_method_var.get()
        payment_method = self.payment_method_var.get()
        date = self.date_input_field.get()

        expenses_details = [amount, currency, category, payment_method, date]
        return expenses_details

    def fetch_data(self, amount, currency):
        while True:
            try:
                amount = float(amount)
                break
            except ValueError:
                print("The amount must be a numeric value!")
                amount = simpledialog.askfloat("Invalid Amount", "Enter a valid numeric amount:")

            if amount <= 0:
                print("The amount must be greater than 0!")
                amount = simpledialog.askfloat("Invalid Amount", "Enter a valid amount greater than 0:")

        # Replace the placeholder API key and adjust the URL accordingly
        url = f"https://api.apilayer.com/fixer/convert?to=USD&from={currency}&amount={amount}"
        headers = {"apikey": "yy7eTIMbsRLnwxHu8WZ7UgsncczcHP7f"}  # Replace with your actual API key

        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print("Sorry, there was a problem. Please try again later.")
            quit()

        result = response.json()
        converted_amount = result.get('result', 0.0)
        return converted_amount

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1000x800")
    expenses_tracker = ExpensesTrackerApp(root)
    root.mainloop()
