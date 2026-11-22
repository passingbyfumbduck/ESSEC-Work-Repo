from abc import ABC, abstractmethod
from typing import final
from xml.etree import ElementTree


class Pipeline(ABC):
    def __init__(self, source):
        self.source = source
        self.data = None

    @final
    def run(self):
        try:
            self.connect()
            self.data = self.extract()
            self.transform(self.data)
            self.validate(self.data)
            self.load(self.data)
            return f"{self.name} Pipeline finished"
        finally:
            self.cleanup()

    def connect(self):
        print(f"Connecting to {self.source}")

    @abstractmethod
    def extract(self):
        pass

    @abstractmethod
    def transform(self, rows):
        pass

    def validate(self, rows):
        for row in rows:
            if not self.required_fields.issubset(row):
                raise ValueError(f"Missing fields: {self.required_fields.difference(row)}")

    def load(self, rows):
        print(f"Loaded {len(rows)} records")

    def cleanup(self):
        self.data = None


class CSVPipeline(Pipeline):
    name = "CSV"
    required_fields = {"id", "name"}

    def extract(self):
        return [{"id": 1, "name": "Alice", "age": "30"}, {"id": 2, "name": "Bob", "age": "25"}]

    def transform(self, rows):
        for row in rows:
            row["age"] = int(row["age"])
            row["name"] = row["name"].upper()


class APIPipeline(Pipeline):
    name = "API"
    required_fields = {"user_id", "username"}

    def extract(self):
        return [
            {"user_id": 101, "username": "Charlie", "score": "85"},
            {"user_id": 102, "username": "Diana", "score": "92"},
        ]

    def transform(self, rows):
        for row in rows:
            row["score"] = int(row["score"])
            row["username"] = row["username"].lower()
            row["grade"] = "A" if row["score"] >= 90 else "B"


class DatabasePipeline(Pipeline):
    name = "Database"
    required_fields = {"product_id", "price"}

    def extract(self):
        return [
            {"product_id": 501, "product_name": "laptop", "price": "1200"},
            {"product_id": 502, "product_name": "mouse", "price": "25"},
        ]

    def transform(self, rows):
        for row in rows:
            row["price"] = float(row["price"])
            row["product_name"] = row["product_name"].title()
            row["tax"] = row["price"] * 0.2


class XMLPipeline(Pipeline):
    name = "XML"
    required_fields = {"order_id", "quantity"}

    def extract(self):
        root = ElementTree.parse(self.source).getroot()
        return [dict(order.attrib) for order in root.findall("order")]

    def transform(self, rows):
        for row in rows:
            row["quantity"] = int(row["quantity"])
