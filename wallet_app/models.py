from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Wallet(db.Model): # создаем можельку кошелька
    __tablename__ = 'wallets'

    uuid = db.Column(db.String(36), primary_key=True)
    balance = db.Column(db.Numeric, default=0)

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if self.balance < amount:
            raise ValueError("Недостаточно средств на счете.")
        self.balance -= amount