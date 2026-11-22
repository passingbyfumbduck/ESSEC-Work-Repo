import json
from pathlib import Path
from threading import Lock


class ConfigManager:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                path = Path(__file__).with_name("config.json")
                if not path.exists():
                    path = path.with_name("config.example.json")
                config = json.loads(path.read_text(encoding="utf-8"))
                instance = super().__new__(cls)
                instance.values = config
                cls._instance = instance
            return cls._instance

    @classmethod
    def get_instance(cls):
        return cls()

    def get(self, key):
        value = self.values
        for part in key.split("."):
            value = value[part]
        return value


def connect_database():
    config = ConfigManager.get_instance()
    print(f"Connecting to database at {config.get('database.host')}:{config.get('database.port')}")


def send_email(to, subject):
    config = ConfigManager.get_instance()
    print(f"Sending {subject} to {to} from {config.get('email.sender')} via {config.get('email.smtp_host')}")


def process_payment(amount):
    config = ConfigManager.get_instance()
    print(f"Processing {amount:.2f} EUR in {config.get('payment.environment')} mode")


def start_application():
    config = ConfigManager.get_instance()
    print(f"Starting {config.get('app.name')} (debug={config.get('app.debug')})")
