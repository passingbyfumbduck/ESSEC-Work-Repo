import csv
import json
from abc import ABC, abstractmethod
from html import escape
from io import StringIO
from pathlib import Path


class FormatStrategy(ABC):
    @abstractmethod
    def render(self, data):
        pass

    def save(self, data, path):
        path.write_text(self.render(data), encoding="utf-8")


class PDFFormatStrategy(FormatStrategy):
    extension = ".pdf"

    def render(self, data):
        rows = [f"| {row['name']:20} | {row['value']:10} |" for row in data]
        return "\n".join(["PDF REPORT", "=" * 50, *rows, "=" * 50, "End of PDF Report"])

    def save(self, data, path):
        from reportlab.pdfgen.canvas import Canvas

        pdf = Canvas(str(path))
        y = 790
        for line in self.render(data).splitlines():
            if y < 50:
                pdf.showPage()
                y = 790
            pdf.setFont("Courier", 10)
            pdf.drawString(40, y, line)
            y -= 16
        pdf.save()


class ExcelFormatStrategy(FormatStrategy):
    extension = ".xlsx"

    def render(self, data):
        rows = [f"{row['name']}\t{row['value']}" for row in data]
        return "\n".join(["EXCEL REPORT", "Name\tValue", *rows])

    def save(self, data, path):
        from openpyxl import Workbook

        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "Sales"
        sheet.append(["Name", "Value"])
        for row in data:
            sheet.append([row["name"], row["value"]])
        workbook.save(path)


class CSVFormatStrategy(FormatStrategy):
    extension = ".csv"

    def render(self, data):
        output = StringIO()
        writer = csv.DictWriter(output, fieldnames=["name", "value"], lineterminator="\n")
        writer.writeheader()
        writer.writerows(data)
        return output.getvalue()


class JSONFormatStrategy(FormatStrategy):
    extension = ".json"

    def render(self, data):
        return json.dumps(data, indent=2)


class HTMLFormatStrategy(FormatStrategy):
    extension = ".html"

    def render(self, data):
        rows = ["<tr><th>Name</th><th>Value</th></tr>"]
        for row in data:
            name = escape(str(row["name"]))
            value = escape(str(row["value"]))
            rows.append(f"<tr><td>{name}</td><td>{value}</td></tr>")
        return "<table>\n" + "\n".join(rows) + "\n</table>"


class ReportGenerator:
    def __init__(self, data):
        self.data = data
        self.strategy = CSVFormatStrategy()

    def set_strategy(self, strategy):
        self.strategy = strategy

    def generate_report(self):
        return self.strategy.render(self.data)

    def save_report(self, filename):
        path = Path(str(filename) + self.strategy.extension)
        self.strategy.save(self.data, path)
        return path
