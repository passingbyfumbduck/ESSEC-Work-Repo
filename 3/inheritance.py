from dataclasses import dataclass


class Vehicle:
    def drive(self):
        return "Driving a vehicle"


class Car(Vehicle):
    def drive(self):
        return "Driving a car"


class Bicycle(Vehicle):
    def drive(self):
        return "Riding a bicycle"


@dataclass
class Person:
    name: str
    age: int
    address: str

    def introduce(self):
        return f"I'm {self.name}, I'm {self.age} and I live at {self.address}."


@dataclass
class Student(Person):
    field_of_study: str

    def introduce(self):
        return f"{super().introduce()} I study {self.field_of_study}."


@dataclass
class Employee(Person):
    company: str

    def introduce(self):
        return f"{super().introduce()} I work at {self.company}."


@dataclass
class BankAccount:
    account_number: str
    balance: float = 0

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit must be positive")
        self.balance += amount

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal must be positive")
        if amount > self.balance:
            return False
        self.balance -= amount
        return True

    def transfer(self, destination, amount):
        if not isinstance(destination, BankAccount):
            raise TypeError("Destination must be a bank account")
        if not self.withdraw(amount):
            return False
        destination.deposit(amount)
        return True


@dataclass
class SavingsAccount(BankAccount):
    interest_rate: float = 0

    def add_interest(self):
        self.balance += self.balance * self.interest_rate

    def check_balance(self):
        return self.balance
