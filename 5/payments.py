from abc import ABC, abstractmethod


class PaymentProcessor(ABC):
    @abstractmethod
    def validate(self, details: dict) -> bool:
        pass

    @abstractmethod
    def process(self, amount: float, details: dict) -> dict:
        pass

    def receipt(self, amount, fee):
        return {"success": True, "method": self.method, "amount": amount + fee, "fee": fee}


class CreditCardProcessor(PaymentProcessor):
    method = "credit_card"

    def validate(self, details):
        number = details.get("card_number")
        cvv = details.get("cvv")
        return (isinstance(number, str) and len(number) == 16 and number.isdigit()
                and isinstance(cvv, str) and len(cvv) == 3 and cvv.isdigit())

    def process(self, amount, details):
        if not self.validate(details):
            number = details.get("card_number")
            if not isinstance(number, str) or len(number) != 16 or not number.isdigit():
                return {"success": False, "error": "Invalid card number"}
            return {"success": False, "error": "Invalid CVV"}
        return self.receipt(amount, amount * 0.029)


class BankTransferProcessor(PaymentProcessor):
    method = "bank_transfer"

    def validate(self, details):
        iban = details.get("iban")
        return isinstance(iban, str) and len(iban) >= 15

    def process(self, amount, details):
        if not self.validate(details):
            return {"success": False, "error": "Invalid IBAN"}
        return self.receipt(amount, 1.50)


class PayPalProcessor(PaymentProcessor):
    method = "paypal"

    def validate(self, details):
        email = details.get("email")
        return isinstance(email, str) and "@" in email

    def process(self, amount, details):
        if not self.validate(details):
            return {"success": False, "error": "Invalid PayPal email"}
        return self.receipt(amount, amount * 0.034 + 0.30)


class PaymentFactory:
    processors = {
        "credit_card": CreditCardProcessor,
        "bank_transfer": BankTransferProcessor,
        "paypal": PayPalProcessor,
    }

    def get_processor(self, payment_type):
        if payment_type not in self.processors:
            raise ValueError(f"Unknown payment type: {payment_type}")
        return self.processors[payment_type]()
