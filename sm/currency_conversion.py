# your_app/templatetags/currency_conversion.py

from django import template
# from currency_converter import CurrencyConverter

# register = template.Library()
# c = CurrencyConverter()

# @register.filter
# def convert_currency(rate, target_currency):
#     # Replace 'INR' with the base currency of your choice
#     base_currency = 'INR'
    
#     if target_currency == base_currency:
#         return rate
    
#     converted_price = c.convert(rate, base_currency, target_currency)
#     return round(converted_price, 2)

import requests
# from tkinter import *
# import tkinter as tk
# from tkinter import ttk
class RealTimeCurrencyConverter():
    def __init__(self,url):
        self.data= requests.get(url).json()
        self.currencies = self.data['rates']



    def convert(self, from_currency, to_currency, amount): 
        initial_amount = amount 
        #first convert it into USD if it is not in USD.
        # because our base currency is USD
        if from_currency != 'USD' : 
            amount = amount / self.currencies[from_currency] 
    
        # limiting the precision to 4 decimal places 
        amount = round(amount * self.currencies[to_currency], 4) 
        return amount