from abc import ABC, abstractmethod
from dataclasses import dataclass


class OrderComponent(ABC):
    @abstractmethod
    def get_cost(self) -> float:
        pass

    @abstractmethod
    def get_description(self) -> str:
        pass

    @property
    @abstractmethod
    def base_price(self) -> float:
        pass


class BaseOrder(OrderComponent):
    def __init__(self, base_price):
        self._base_price = base_price

    @property
    def base_price(self):
        return self._base_price

    def get_cost(self):
        return self.base_price

    def get_description(self):
        return f"Base order ({self.base_price:.2f} EUR)"


@dataclass
class OrderDecorator(OrderComponent):
    order: OrderComponent

    @property
    def base_price(self):
        return self.order.base_price

    def get_description(self):
        return f"{self.order.get_description()}, {self.label}"


class ExpressShippingDecorator(OrderDecorator):
    label = "express shipping"

    def get_cost(self):
        return self.order.get_cost() + 15


class InsuranceDecorator(OrderDecorator):
    label = "insurance (5% of base price)"

    def get_cost(self):
        return self.order.get_cost() + self.base_price * 0.05


class GiftWrapDecorator(OrderDecorator):
    label = "gift wrap"

    def get_cost(self):
        return self.order.get_cost() + 5


@dataclass
class DiscountDecorator(OrderDecorator):
    percent: float

    @property
    def label(self):
        return f"{self.percent}% discount"

    def get_cost(self):
        return self.order.get_cost() * (1 - self.percent / 100)


class PremiumMemberDecorator(DiscountDecorator):
    def __init__(self, order):
        super().__init__(order, 10)

    label = "premium member discount (10%)"
