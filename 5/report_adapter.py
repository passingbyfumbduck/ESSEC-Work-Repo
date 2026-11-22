import json
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod


class LegacyReportGenerator:
    def generate_report(self, data: dict) -> str:
        xml = "<report>\n"
        for key, value in data.items():
            xml += f"  <{key}>{value}</{key}>\n"
        return xml + "</report>"


class ReportGeneratorInterface(ABC):
    @abstractmethod
    def generate(self, data: dict) -> str:
        pass


class LegacyReportAdapter(ReportGeneratorInterface):
    def __init__(self, legacy):
        self.legacy = legacy

    def generate(self, data):
        root = ET.fromstring(self.legacy.generate_report(data))
        report = {}
        for field in root:
            text = field.text or ""
            try:
                value = json.loads(text)
            except ValueError:
                value = text
            report[field.tag] = value
        return json.dumps(report)


class AnalyticsDashboard:
    def display(self, json_data):
        print("=== Analytics Dashboard ===")
        for name, value in json.loads(json_data).items():
            print(f"  {name}: {value}")
