from dataclasses import dataclass, replace


@dataclass
class Employee:
    first_name: str = ""
    last_name: str = ""
    email: str = ""
    department: str = ""
    position: str = ""
    salary: float = 0
    start_date: str | None = None
    manager_id: int | None = None
    phone: str | None = None
    address: str | None = None
    emergency_contact: str | None = None
    has_parking: bool = False
    has_laptop: bool = False
    has_vpn_access: bool = False
    has_admin_rights: bool = False
    office_location: str | None = None
    contract_type: str = "permanent"


class EmployeeBuilder:
    def __init__(self):
        self.employee = Employee()

    def with_name(self, first, last):
        self.employee.first_name = first
        self.employee.last_name = last
        return self

    def with_email(self, email):
        self.employee.email = email
        return self

    def with_job(self, department, position, salary):
        self.employee.department = department
        self.employee.position = position
        self.employee.salary = salary
        return self

    def with_equipment(self, *, laptop=False, parking=False):
        self.employee.has_laptop = laptop
        self.employee.has_parking = parking
        return self

    def with_access(self, *, vpn=False, admin=False):
        self.employee.has_vpn_access = vpn
        self.employee.has_admin_rights = admin
        return self

    def with_contract(self, start_date, contract_type="permanent"):
        self.employee.start_date = start_date
        self.employee.contract_type = contract_type
        return self

    def with_office(self, location, manager_id=None):
        self.employee.office_location = location
        self.employee.manager_id = manager_id
        return self

    def with_contact(self, *, phone=None, address=None, emergency_contact=None):
        self.employee.phone = phone
        self.employee.address = address
        self.employee.emergency_contact = emergency_contact
        return self

    def build(self):
        employee = self.employee
        if not employee.first_name or not employee.last_name:
            raise ValueError("Name is required")
        if "@" not in employee.email:
            raise ValueError("Valid email is required")
        if employee.salary < 0:
            raise ValueError("Salary cannot be negative")
        return replace(employee)


class DeveloperBuilder(EmployeeBuilder):
    def __init__(self, first, last, email):
        super().__init__()
        self.with_name(first, last).with_email(email)
        self.with_job("Engineering", "Senior Developer", 75000)
        self.with_equipment(laptop=True).with_access(vpn=True, admin=True)
