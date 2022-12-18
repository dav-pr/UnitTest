"""
A very advanced employee management system

"""

import logging
from dataclasses import dataclass

from typing import List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.INFO)


# noinspection PyTypeChecker
@dataclass
class Employee:
    """Basic employee representation"""

    first_name: str
    last_name: str
    role: str
    vacation_days: int = 25

    @property
    def fullname(self):
        return self.first_name, self.last_name

    def __str__(self) -> str:
        """Return a string version of an instance"""

        return str(self.fullname)

    def take_holiday(self, payout: bool = False) -> None:
        """Take a single holiday or a payout vacation"""

        remaining = self.vacation_days
        if payout:
            if self.vacation_days < 5:
                msg = f"{self} have not enough vacation days. " \
                      f"Remaining days: %d. Requested: %d" % (remaining, 5)
                raise ValueError(msg)
            self.vacation_days -= 5
            msg = "Taking a holiday. Remaining vacation days: %d" % remaining
            logger.info(msg)
        else:
            if self.vacation_days < 1:
                remaining = self.vacation_days
                msg = f"{self} have not enough vacation days. " \
                      f"Remaining days: %d. Requested: %d" % (remaining, 1)
                raise ValueError(msg)
            self.vacation_days -= 1
            msg = "Taking a payout. Remaining vacation days: %d" % remaining
            logger.info(msg)


# noinspection PyTypeChecker
@dataclass
class HourlyEmployee(Employee):
    """Represents employees who are paid on worked hours base"""

    amount: int = 0
    hourly_rate: int = 50

    def log_work(self, hours: int) -> None:
        """Log working hours"""

        self.amount += hours


# noinspection PyTypeChecker
@dataclass
class SalariedEmployee(Employee):
    """Represents employees who are paid on a monthly salary base"""

    salary: int = 5000


# noinspection PyTypeChecker
class Company:
    """A company representation"""

    def __init__(self, title: str, employees: List[Employee]):
        if self.validate(title, employees):
            self.title = title
            self.employees = employees

    def __repr__(self):
        return self.title

    def __str__(self):
        return self.title

    @staticmethod
    def validate(title, employees):
        """Функція перевіряє вхідний параметр на відповідність типам вхідних даних"""

        res = True
        if not isinstance(title.strip(), str):
            res = False
        for i in title:
            if i.isalnum():
                res = True
                break
        for employee in employees:
            if not isinstance(employee, Employee):
                res = False
        return res

    def get_employees_by_role(self, employee_role: str) -> List[Employee]:
        """
        :param employee_role:
        :return:
        Creating employees list according to the role
        """
        return list(filter(lambda x: x.role == employee_role, self.employees))

    def get_ceos(self) -> List[Employee]:
        """Return employees list with role of CEO"""

        employee_role = "CEO"
        return self.get_employees_by_role(employee_role)

    def get_managers(self) -> List[Employee]:
        """Return employees list with role of manager"""

        employee_role = "manager"
        return self.get_employees_by_role(employee_role)

    def get_developers(self) -> List[Employee]:
        """Return employees list with role of developer"""

        employee_role = "dev"
        return self.get_employees_by_role(employee_role)

    @staticmethod
    def pay(employee: Employee) -> None:
        """Pay to employee"""

        if isinstance(employee, SalariedEmployee):
            msg = f"Paying monthly salary of {employee.salary:.2f} to {employee}"
            logger.info(msg)

        if isinstance(employee, HourlyEmployee):
            msg = f"Paying {employee} hourly rate of " \
                  f"{employee.hourly_rate:.2f} for {employee.amount} hours"
            logger.info(msg)

    def pay_all(self) -> None:
        """Pay all the employees in this company"""

        for employee in self.employees:
            self.pay(employee)
