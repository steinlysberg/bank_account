#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 10:38:05 2024

@author: steinlysberg
"""

from time import strftime, time
from functools import wraps
from random import randint

def history_decorator(func):
    @wraps(func)
    def inner(self, amount):
        old_balance = self.balance
        result = func(self, amount)
        new_balance = self.balance
        transaction_type = None
        if new_balance > old_balance:
            transaction_type = "Deposit"
        elif new_balance < old_balance:
            transaction_type = "Withdrawal"
        if transaction_type:
            self.transactions.append({"date_and_time": strftime("%Y/%m/%d %H:%M:%S"),
                                    "amount": amount,
                                    "transaction_type": transaction_type})
        return result
    return inner
    
def balance_decorator(func):
    @wraps(func)
    def inner(self, amount):
        if amount > self.balance:
            print("Withdrawal denied due to insufficient funds.")
            amount = 0
            return func(self, amount)
        else:
            print("Withdrawal successful.")
            return func(self, amount)
    return inner
    
def timer_decorator(func):
        @wraps(func)
        def inner(self, *args, **kwargs):
            start_time = time()
            result = func(self, *args, **kwargs)
            end_time = time()
            print(f"Execution time for {func.__name__}: {(end_time - start_time)*1000000:.02f} µs")
            return result
        return inner

class BankAccount:
    
    def __init__(self, init_balance, account_number = randint(1, 1000000)):
        self.account_number = account_number
        self.balance = init_balance
        self.transactions = []
        self.transactions.append({"date_and_time": strftime("%Y/%m/%d %H:%M:%S"),
                                  "amount": init_balance,
                                  "transaction_type": "Initial deposit"})
        self.closed = False
    
    @timer_decorator        
    @history_decorator
    def deposit(self, amount):
        self.balance += amount
        print("Deposit successful.")
    
    @timer_decorator    
    @balance_decorator
    @history_decorator
    def withdraw(self, amount):
        self.balance -= amount
    
    def balance_inquiry(self):
        return f"Current balance is {self.balance}."

    def get_transactions(self):
        result = ""
        for i in self.transactions:
            result += "\nDate and time: " + i["date_and_time"]
            result += "\nTransaction type: " + i["transaction_type"]
            result += "\nAmount: " + str(i["amount"]) + "\n"
        return result
    
    def get_statement(self):
        result = ""
        result += ("\nTRANSACTIONS:\n")
        result += (self.get_transactions())
        result += ("\nCURRENT BALANCE:\n\n")
        result += str(self.balance)
        return result
        
    def get_summary(self):
        result = ""
        result += (f"\nACCOUNT NUMBER: {self.account_number}\n")
        result += (f"CURRENT BALANCE: {self.balance}\n")
        result += (f"NUMBER OF TRANSACTIONS: {(len(self.transactions))}")
        return result

    def account_closure(self):
        self.balance = None
        self.transactions = None
        self.closed = True
    
    def is_account_closed(self):
        return self.closed and not self.transactions and not self.balance
    
def User_menu():
    account = None
    account_open = False

    while True:
        print("\nBank Account Management System\n")
        print("1.\tCreate Account")
        print("2.\tDeposit Money")
        print("3.\tWithdraw Money")
        print("4.\tCheck Balance")
        print("5.\tView Transaction History")
        print("6.\tGenerate Account Statement")
        print("7.\tGenerate Account Summary")
        print("8.\tClose Account")
        print("9.\tCheck if Account is Closed")
        print("X.\tExit  \n" )
        
        user_input = input("Choose an option from the menu: " ) 
        
        if user_input == "1":
           balance = float(input("Enter yout intial balance: "))
           account = BankAccount(balance)
           print("\nAccount created.")
           print(f"Account number: {account.account_number}")
           print(f"Initial balance: {account.balance}")
           account_open = True
          
        elif user_input == "9" and account:
            if(account.is_account_closed()):
                print(f"Account {account.account_number} is closed.")
            else:
                print(f"Account {account.account_number} is not closed.")
        
        elif account and not account_open:
            print("No account is open. Action not possible.")
        
        elif user_input == "2" and account:
             amount = input("Enter the amount you want to deposit: ")
             try:
                 amount = float(amount)
             except:
                 print("Input must be a number.")
             else:
                 if amount >= 0:
                     account.deposit(float(amount))
                 else:
                     print("Input can not be negative. Use withdrawal instead.")
           
        elif user_input == "3" and account:
             amount = input("Enter the amount you want to withdraw: ")
             try:
                 amount = float(amount)
             except:
                 print("Input must be a number.")
             else:
                 if amount >= 0:
                     account.withdraw(float(amount))
                 else:
                     print("Input can not be negative. Use deposit instead.")
             
        elif user_input == "4" and account:
             print(account.balance_inquiry())
        
        elif user_input == "5" and account:        
             print(account.get_transactions())
             
        elif user_input == "6" and account:
            print(account.get_statement())
        
        elif user_input == "7" and account:
            print(account.get_summary())
        
        elif user_input == "8" and account:
            print(f"Closing account {account.account_number}.")
            account.account_closure()
            account_open = False
                
        elif user_input == "x" or user_input == "X":
            print("Exiting the bank.") 
            break
        else: 
            if not account:
                print("No account created yet! Create an account first.\n")
            else:
                print("Invalid option. Try again.\n")
    
User_menu()