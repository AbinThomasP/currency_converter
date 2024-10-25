import tkinter as tk
import requests

# Extended list of currencies
common_currencies = ['USD', 'EUR', 'GBP', 'JPY', 'CAD', 'AUD', 'CHF', 'NZD', 'INR', 'ZAR', 'MXN', 'CNY', 'SGD']

# Fixer.io API key (replace with your own key)
API_KEY = '5900db18f73ee6a890e71fc3d0dc368c'
# 926bdd32ce58ae9d263491a4fc044fad
class CurrencyConverter:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Currency Converter')
        self.root.geometry('300x300')

        self.from_var = tk.StringVar(self.root)
        self.from_var.set('USD')
        self.from_menu = tk.OptionMenu(self.root, self.from_var, *common_currencies)
        self.from_menu.pack(pady=1)

        self.to_var = tk.StringVar(self.root)
        self.to_var.set('INR')
        self.to_menu = tk.OptionMenu(self.root, self.to_var, *common_currencies)
        self.to_menu.pack(pady=1)

        self.amount_label = tk.Label(self.root, text='Amount:')
        self.amount_label.pack(pady=2)

        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.pack(pady=2)

        self.convert_button = tk.Button(self.root, text='Convert', command=self.convert_currency)
        self.convert_button.pack(pady=2)
        self.result_label = tk.Label(self.root, text="")
        self.result_label.pack(pady=1)

        self.root.mainloop()

    def convert_currency(self):
        try:
            from_currency = self.from_var.get()
            to_currency = self.to_var.get()
            amount_str = self.amount_entry.get()

            # Check if the input is empty or contains only whitespace
            if not amount_str.strip():
                self.result_label.config(text='Amount cannot be empty!')
                return

            # Ensure the input is numeric
            try:
                amount = float(amount_str)
            except ValueError:
                self.result_label.config(text='Please enter a valid number!')
                return

            # Perform the conversion using Fixer.io API
            url = f'http://data.fixer.io/api/latest?access_key={API_KEY}&symbols={to_currency},{from_currency}'
            response = requests.get(url)
            data = response.json()

            if data.get('success') is False:
                self.result_label.config(text=f"Error: {data.get('error', {}).get('info', 'API error')}")
                return

            # Get exchange rate and perform the conversion
            rates = data['rates']
            if from_currency == 'EUR':  # Fixer.io's base currency is EUR
                rate = rates[to_currency]
            else:
                rate = rates[to_currency] / rates[from_currency]

            converted_amount = amount * rate
            self.result_label.config(text=f'{amount} {from_currency} = {converted_amount:.2f} {to_currency}')

        except Exception as e:
            self.result_label.config(text=f'Error: {e}')


if __name__ == '__main__':
    CurrencyConverter()








