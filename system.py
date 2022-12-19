"""
A very advanced employee management system

"""

from abc import abstractmethod
from dataclasses import dataclass
import re
import logging
from typing import List
from settings import Param, LogParam

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(LogParam.NAME_LOGGER.value)
logger.setLevel(logging.INFO)


# TODO
@dataclass
class Role:
    """
    Клас посада. Саме така реілізація, коли клас містить лише атрибут найменування посади, є спорною.
    Такий клас повинен містити і інші ознаки посади, наприклад, посадовий оклад. Тоді цей клас наповнюється змістом.

    """
    role: str

    def __init__(self, role: str) -> None:

        if self.validate_name(role):
            self.role = role.strip()
        else:
            raise ValueError(f"{self} Name of role does not meet the requirements: {role}")

    @staticmethod
    def validate_name(role: str) -> bool:
        """

        :param role: str
        :return:
        Валідація найменування посади.
        """
        return isinstance(role, str) and role.strip().isalpha()

    def __eq__(self, other) -> bool:
        """

        :param other:
        :return:
        Без коментарів
        """
        if isinstance(other, str):
            return self.role == other
        elif isinstance(other, Role):
            return self.role == other.role
        else:
            raise TypeError


# noinspection PyTypeChecker

class Roles:
    """
    Реалізація явища "штатний розпис", а по факту список посад.
    Клас створений для контролю за відсутність дублікатів назв посад у компанії.
    """

    def __init__(self) -> None:
        self.list_of_roles: List[Role] = []

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self)-> Role:

        if self.index < len(self.list_of_roles):
            self.index += 1
            return self.list_of_roles[self.index - 1]
        else:
            raise StopIteration

    def add_role(self, role_inst: Role, warning=True) -> None:
        """

        :param role_inst: екземпляр класу Role
        :param warning: ознака чи здійснювати зупинку обрабки посади, у випадку виявлення дубліката найменування посади.
                        Якщо True - така зупинка здіснюється
        :return:
        """
        if isinstance(role_inst, str):
            role_inst = Role(role_inst)
        if role_inst not in self.list_of_roles:
            self.list_of_roles.append(role_inst)
        else:
            if warning:
                msg = f"{self} Role already exists: {role_inst}"
                raise ValueError(msg)


# noinspection PyTypeChecker
@dataclass
class Employee:
    """Basic employee representation"""

    first_name: str
    last_name: str
    role: str
    # початкове значення тривалості відпустки Param.VCTN_DAYS_INI
    vacation_days: int = Param.VCTN_DAYS_INI

    def __init__(self, first_name: str, last_name: str, role: str, vacation_days=Param.VCTN_DAYS_INI):
        """

        :param first_name: ім'я
        :param last_name: прізвище
        :param role: посада (потребує доопрацювання, а саме логіно передавати Role instance)
        :param vacation_days: Param.VCTN_DAYS_INI  # початкове значення тривалості відпустки
        Ініціалізація параметров та виклик функції, яка виконує валідацію значень.
        !!! Метод автоматично перетворює ім'я та прізвище у формат capitalize()
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
            msg = f"{other} is not Employee type"
            raise ValueError(msg)

    @property
    def fullname(self):
        return self.first_name, self.last_name

    def __str__(self) -> str:
        """Return a string version of an instance"""

        return " ".join(self.fullname)

    @abstractmethod
    def pay(self):
        """

        :return:
        Абстрактний метод для виплати заробітної плати. Перенесений із класу Company. Його місце тут.
        """
        ...

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
            msg = f"{self} sum amount and hours > Param.AMOUNT_LIMIT = {Param.AMOUNT_LIMIT} " \
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

    def pay(self):
        msg = ("Paying %s hourly rate of %.2f for %d hours") % (self, self.hourly_rate, self.amount)
        logger.info(msg)


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

    def pay(self):
        msg = ("Paying monthly salary of %.2f to %s") % (self.salary, self)
        logger.info(msg)


# noinspection PyTypeChecker
class Company:
    """A company representation"""

    def __init__(self, title: str):
        """"""
        if self.validate_name(title):
            self.title = title.strip()
            self.employees = []
            self.roles = Roles()
        else:
            msg = f"{self} Not valid title: {title}"
            raise ValueError(msg)


    @staticmethod
    def validate_employees(employees: List[Employee]) -> bool:
        """Функція перевіряє вхідний параметр на відповідність типам вхідних даних.
        """
        if employees is not None:
            for item in employees:
                if not isinstance(item, Employee):
                    return False
            return True
        else:
            return True

    @staticmethod
    def validate_name(name: str) -> bool:
        """

        :param name: найменування компанії
        :return:
        Найбільш спірна реалізація. Трохи хаотична.
        Логіка: якщо є заборонене сімволи у назві команії, які визначаються match, то повертається False.
        Якщо після видалення з найменування дозволених символів legal_symb строка не відповідає вимогам isidentifier(),
        то також повертається False
        """

        if isinstance(name, str):
            bad_name = False
            name = name.strip()
            match = re.search(r'[~@#$%^*()_+|{}"?><]', name)
            legal_symb = [",", ".", ':', ';', '!', '&', '?', " "]
            copy_name = name
            for symb in legal_symb:
                copy_name = copy_name.replace(symb, '')
            bad_name = not copy_name.isidentifier()
            if match or name == '':
                bad_name = True
            return not bad_name
        else:
            return False

    def add_roles(self, *args,  warning=True) -> None:
        """

        :param args: UNIT[str, Role, Roles]
        :param warning: визначає чи зупиняти виконання у випадку виявлення дублікату найменування посади.
        !!! Незалежно від параметру  warning дублікати посади не будуть додані до списку посад.
        :return:
        Метод здійснює додавання посад до компанії.

        """
        for arg in args:
            if isinstance(arg, str):
                inst_role = Role(arg)
                self.roles.add_role(inst_role, warning=warning)

            elif isinstance(arg, Role):
                self.roles.add_role(arg, warning=warning)

            elif isinstance(arg, Roles):
                for item in arg:
                    self.roles.add_role(item, warning=warning)

    def add_employee(self, *args):
        """
        :param args:
        :return:
        Метод здійснює додавання працівника до списку працівників компанії.
        Метод здійснює контроль щодо неможливості додати працівника з таким самим іменем та прізвищем.
        !!! Повідомлення про відмову додати дублікат працівника не реаоізовано.
        """
        for arg in args:
            if isinstance(arg, Employee):
                if arg not in self.employees:
                    self.employees.append(arg)
            else:
                msg = f"{arg} is not type Employee"
                raise ValueError

    def isrole(self, name_role: str) -> bool:
        """

        :param name_role:
        :return:
        Метод повертає озанку чи є посада name_role у списку посад
        """
        return name_role in self.roles

    def add_roles_from_employees(self, emp_instance: List[Employee]) -> None:
        """

        :param emp_instance:
        :return:
        Додає працівників до компанії
        """

        for item in emp_instance:
            if isinstance(item, Employee):
                self.roles.add_role(item.role)

    def get_employees_by_role(self, employee_role: str) -> List[Employee]:
        """
        :param employee_role:
        :return:
        Повртає список працівників за ознакою посади
        """
        return list(filter(lambda x: x.role == employee_role, self.employees))



    def pay_all(self) -> None:
        """

        :return:
        Метод заплатити усім.
        Той хто дочитав до цього місця, може отримати пляшку Chivas Regal, метро Палац спорту, Київ, до 25.12.2022
        """
        for item in self.employees:
            item.pay()
