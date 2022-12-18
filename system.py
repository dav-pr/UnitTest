"""
A very advanced employee management system

"""

import logging
from dataclasses import dataclass
from typing import List
from settings import Param, LogParam

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(LogParam.NAME_LOGGER.value)
logger.setLevel(logging.INFO)


# TODO
@dataclass
class Role:
    role: str

    def __init__(self, role: str) -> None:

        if self.validate_name(role):
            self.role = role.strip()
        else:
            raise ValueError(f"{self} Name of role does not meet the requirements: {role}")

    @staticmethod
    def validate_name(role: str) -> bool:
        return isinstance(role, str) and role.strip().isalpha()

    def __eq__(self, other):
        if isinstance(other, str):
            return self.role == other
        elif isinstance(other, Role):
            return self.role == other.role
        else:
            raise TypeError


# noinspection PyTypeChecker

class Roles:
    list_of_roles: List[Role] = []

    def add_role(self, name_role: str) -> None:
        role_inst = Role(name_role)
        if role_inst not in self.list_of_roles:
            self.list_of_roles.append(role_inst)
        else:
            msg = f"{self} Role already exists: {name_role}"
            raise ValueError(msg)


# noinspection PyTypeChecker
@dataclass
class Employee:
    """Basic employee representation"""

    first_name: str
    last_name: str
    role: str
    vacation_days: int = Param.VCTN_DAYS_INI

    def __init__(self, first_name: str, last_name: str, role: str, vacation_days=Param.VCTN_DAYS_INI):
        """

        :param first_name:
        :param last_name:
        :param role:
        :param vacation_days:
        Ініціалізація параметров та виклик функції, яка виконує валідацію значень.

        """

        if self.validate_str(first_name, last_name, role) and self.valadate_vacation_days(vacation_days):
            self.first_name = first_name.strip().capitalize()
            self.last_name = last_name.strip().capitalize()
            self.role = role.strip()
            self.vacation_days = vacation_days

        else:
            msg = f"None validate names or vacation_days."
            raise ValueError(msg)

    def __eq__(self, other) -> bool:

        if isinstance(other, Employee):
            return self.first_name == other.first_name and self.last_name == other.last_name

        else:
            msg=f"{other} is not Employee type"
            raise ValueError(msg)

    @property
    def fullname(self):
        return self.first_name, self.last_name

    def __str__(self) -> str:
        """Return a string version of an instance"""

        return " ".join(self.fullname)

    @staticmethod
    def validate_str(*args) -> bool:
        """
        :param param: вхідний парамерт
        :return: True, якщо відповідає вимогам.

        Функція перевіряє вхідний параметр на відповідність типу та вимогам до написання імені особи.
        """
        res = True
        for arg in args:
            res = res and isinstance(arg, str) and arg.strip().isalpha()
        return res

    @staticmethod
    def valadate_vacation_days(days: int):
        """

        :param days:
        :return:
        Функція виконує валідацію кількості днів відпустки
        """
        return isinstance(days, int) and days > -1 and days < 32

    def taking_holiday(self, num_days=Param.HLD_MIN_DAY.value) -> None:
        """

        :param num_days: кількість днів відпустки, що береться
        :return:
        Функція виконує процедуру надання певних днів відпустки. Кількість днів відпустки, що
        береться визначається параметром num_days. Мінімальна кількість днів відпустки, що
        може бути надана визначається параметром Param.HLD_MIN_DAY.value.
        У процесі виконання здійснюється перевірки чи залишок відпустки не меньше кількості днів,
        що запитується та чи не меньше кількість днів, що запитується мінімальної кількості днів
        відпустки, що може бути надана. Якщо умова не дотримується, то здійснюється формування
        відповідного повідомлення та викликається raise ValueError(msg). Якщо умови дотримані, то
        залишок відпустки зменшується на num_days, та здійснюється запис у логер.
        """

        if num_days >= Param.HLD_MIN_DAY and not self.vacation_days < num_days:
            self.vacation_days -= num_days
            msg = f"Taking a holiday {num_days}. Remaining vacation days: {self.vacation_days}"
            logger.info(msg)
        else:
            if not num_days >= Param.HLD_MIN_DAY:
                msg = f"{self} have not enough vacation days. " \
                      f"Remaining days: {self.vacation_days}. Requested: {num_days}"
            elif self.vacation_days < num_days:
                msg = f"{self} Requested minimum possible . " \
                      f" Minimum  requested days: {Param.HLD_MIN_DAY} " \
                      f"Requested: {num_days}"
            raise ValueError(msg)

    def taking_payout(self, num_days=1) -> None:
        """

        :param num_days: кількість днів, за які отримується грошова компенсація
        :return:
        Функція здійснює зменьшення залишку відпустки шляхом її зменьшення за рахунок днів, за які
        отримано грошову компенсацію.
        Кількість днів, за яку надається грошова компенсація визначається  аргументом num_days.
        У процесі виконання тіла функції здійснюється перевірка чи num_days більше нуля, та чи
        не більше  залишку днів  відпустки.  Якщо умови дотримані, то
        залишок відпустки зменшується на num_days, та здійснюється запис у логер.
        Якщо умова не дотримується, то здійснюється формування
        відповідного повідомлення та викликається raise ValueError(msg)

        """

        if not self.vacation_days < num_days and num_days > 0:
            self.vacation_days -= num_days
            msg = f"Taking a payout {num_days}. Remaining vacation days: {self.vacation_days}"
            logger.info(msg)
        else:
            if self.vacation_days < num_days:
                msg = f"{self} have not enough vacation days. " \
                      f"Remaining days: {self.vacation_days}. Requested:{num_days}"
            elif not num_days > 0:
                msg = f"{self} Requested minimum possible . " \
                      f" Minimum  requested days: 1 " \
                      f"Requested: {num_days}"

            raise ValueError(msg)

    def take_holiday(self, payout: bool = False) -> None:
        """Take a single holiday or a payout vacation"""
        # TODO
        # функція іде на виліт, як не потрібна

        if payout:
            self.taking_holiday()
        else:
            self.taking_payout()

        # noinspection PyTypeChecker


@dataclass
class HourlyEmployee(Employee):
    """Represents employees who are paid on worked hours base"""

    amount: int = 0
    hourly_rate: int = Param.HOURLY_RATE

    def raise_hours_log_work(self, hours: int) -> None:
        """

        :param hours: кількість годин, яка додається до відпрацьованих
        :return:
        Метод формує повідомлення про причини експшена та викликає raise ValueError(msg).
        Кількість відпрацьованих годин не може бути меньше 0 та перевищувати ліміт встановлений
        параметром Param.HOURLY_RATE.
        """

        if hours < 0:
            msg = f"{self} hours < 0." \
                  f"Requested hours:{hours}"
        else:
            if hours > Param.HOURLY_RATE:
                msg = f"{self} hours > {Param.HOURLY_RATE}." \
                      f"Requested hours:{hours}"
            else:
                msg = f"Type of hours not valid. Must \"int\", requested {type(hours)}"
        raise ValueError(msg)

    def check_limit_log_work(self, hours) -> None:
        """

        :param hours: кількість годин, яка додається до відпрацьованих
        :return:

        Параметров AMOUNT_LIMIT = 302 встановний ліміт годин, які максимально може
        відпрацювати працівників. Метод перевіряє чи не перевіщується такий ліміт, у випадку
        перевищення - raise ValueError(msg)
        """

        if self.amount + hours > Param.AMOUNT_LIMIT:
            msg = f"{self} sum amount and hours > Param.AMOUNT_LIMIT = {Param.AMOUNT_LIMIT}" \
                  f"Amount hours: {self.amount}. Requested hours:{hours}"
            raise ValueError(msg)

    def log_work(self, hours: int) -> None:
        """Log working hours"""
        self.check_limit_log_work(hours)
        if isinstance(hours, int) and hours > 0 and not hours > Param.HOURLY_RATE:
            self.amount += hours
            msg = f"Employee {self.fullname} amount {hours}. Full amount {self.amount}"
            logger.info(msg)
        else:
            self.raise_hours_log_work(hours)


# noinspection PyTypeChecker
@dataclass
class SalariedEmployee(Employee):
    """Represents employees who are paid on a monthly salary base
    Максимальний розмір  salary обмежений параметром Param.SALARY_LIMIT.
    Salary може дорівнювати Param.SALARY_LIMIT, але не може бути більше його.

    """

    salary: int = Param.SALARY_DEFAULT

    def __init__(self, first_name: str, last_name: str, role: str, vacation_days=Param.VCTN_DAYS_INI,
                 salary=Param.SALARY_DEFAULT):
        """

        :param first_name:
        :param last_name:
        :param role:
        :param vacation_days:
        :param salary:
        """
        super().__init__(first_name, last_name, role, vacation_days)
        if self.validate_salary(salary):
            self.salary = salary
        else:
            msg = f"{self} Salary does not meet the requirements"
            raise ValueError(msg)

    @staticmethod
    def validate_salary(salary):
        """

        :return:
        Атрибут salary класу SalariedEmployee повинен перебувати у діапазоні від 1 (включно) до
        Param.SALARY_LIMIT (включно). Також  атрибут salary класу SalariedEmployee повинен бути типу int.
        У випадку відповідності цим умовам метод повертає True, у протилежному випадку провертає False.
        """
        return isinstance(salary, int) and salary > 0 and not salary > Param.SALARY_LIMIT


# noinspection PyTypeChecker
class Company:
    """A company representation"""

    def __init__(self, title: str, employees: List[Employee] = None):
        if self.validate_name(title):
            self.title = title.strip()
        else:
            msg=f"{self} Not valid title: {title}"
            raise ValueError(msg)
        if self.validate_employees(employees):
            if employees is None:
                self.employees =[]
            else:
                self.employees = employees


    @staticmethod

    def validate_employees(employees:List[Employee]) -> bool:
        """Функція перевіряє вхідний параметр на відповідність типам вхідних даних"""
        if employees is not None:
            for item in employees:
                if not isinstance(item,Employee):
                    return False
            return True
        else:
            return True

    @staticmethod
    def validate_name(name: str) -> bool:
        return isinstance(name, str) and name.strip().isalnum()

    def add_employee(self, *args):
        for arg in args:
            if isinstance(arg, Employee):
                if arg not in self.employees:
                    self.employees.append(arg)
            else:
                msg=f"{arg} is not type Employee"
                raise ValueError



    def get_employees_by_role(self, employee_role: str) -> List[Employee]:
        """
        :param employee_role:
        :return:
        Creating employees list according to the role
        """
        return list(filter(lambda x: x.role == employee_role, self.employees))

    def get_ceos(self) -> List[Employee]:
        """Return employees list with role of CEO"""

        result = []
        for employee in self.employees:
            if employee.role == "CEO":
                result.append(employee)
        return result

    def get_managers(self) -> List[Employee]:
        """Return employees list with role of manager"""

        result = []
        for employee in self.employees:
            if employee.role == "manager":
                result.append(employee)
        return result

    def get_developers(self) -> List[Employee]:
        """Return employees list with role of developer"""

        result = []
        for employee in self.employees:
            if employee.role == "dev":
                result.append(employee)
        return result

    @staticmethod
    def pay(employee: Employee) -> None:
        """Pay to employee"""

        if isinstance(employee, SalariedEmployee):
            msg = (
                      "Paying monthly salary of %.2f to %s"
                  ) % (employee.salary, employee)
            logger.info(f"Paying monthly salary to {employee}")

        if isinstance(employee, HourlyEmployee):
            msg = (
                      "Paying %s hourly rate of %.2f for %d hours"
                  ) % (employee, employee.hourly_rate, employee.amount)
            logger.info(msg)

    def pay_all(self) -> None:
        """Pay all the employees in this company"""

        # TODO: implement this method
