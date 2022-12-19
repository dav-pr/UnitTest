import random
import unittest
import system as sm
from settings import Param, LogParam


class EmployeeTest(unittest.TestCase):
    """
    реалізвація тестов для класа Employee
    bad_str містить строки, які не можуть бути використані для імен працівників
    good_str - містить строки, які можуть бути використані. Строки " Bond", " Bond ", "Bond "
    можуть подаватись на вхід, це ну буде викликати помилки, у методах класу реалізований strip()
    """
    bad_str = ["", "Bond1", "1bond", "david@", "@david", "111", 1, 1.68]
    good_str = ["Bond", "David", "Dev", " Bond", " Bond ", "Bond "]

    def test_ini(self):
        """
        :return:
        Тестування правильності ініціалізації параметров.
        Даний тест не виконує валідацію введених даний, а просто перевіряя правильність передачі даних при ініціалізації
        """
        self.instance = sm.Employee("David", "Bond", "DEV", 1)
        self.assertEqual("David", self.instance.first_name)
        self.assertEqual("Bond", self.instance.last_name)
        self.assertEqual("DEV", self.instance.role)
        self.assertEqual(1, self.instance.vacation_days)
        self.instance = sm.Employee("David", "Bond", "Dev")
        # перевірки ініціалізації vacation_days по замовченню
        self.assertEqual(25, self.instance.vacation_days)

        # перевірка роботи capitalize()
        self.instance = sm.Employee("david", "bond", "dev")
        self.assertNotEqual("david", self.instance.first_name)
        self.assertNotEqual("bond", self.instance.last_name)
        self.assertEqual("dev", self.instance.role)

        # перевірка роботи strip()
        self.instance = sm.Employee("  David ", " bond ", " Dev ")
        self.assertEqual("David", self.instance.first_name)
        self.assertEqual("Bond", self.instance.last_name)
        self.assertEqual("Dev", self.instance.role)

    def test_validate(self):
        """

        :return:
        Тестування методу valadate_vacation_days().

        """

        bad_days = [-1, 32, 99, 100]
        for i in bad_days:
            with self.assertRaises(ValueError):
                sm.Employee("David", "Bond", "Dev", i)

        for i in range(1, 32):
            # памєятаємо, що 32 не включається
            self.instance = sm.Employee("David", "Bond", "Dev", i)
            self.assertEqual(i, self.instance.vacation_days)

        # тестування спрацювання raise (ValueError)

        for good_item in self.good_str:
            for item in self.bad_str:
                with self.assertRaises(ValueError):
                    sm.Employee(item, good_item, good_item, 1)

        for good_item0 in self.good_str:
            for good_item1 in self.good_str:
                for good_item2 in self.good_str:
                    instance = sm.Employee(good_item0, good_item1, good_item2, 1)
                    self.assertEqual(good_item0.strip(), instance.first_name)
                    self.assertEqual(good_item1.strip(), instance.last_name)
                    self.assertEqual(good_item2.strip(), instance.role)

    def test_full_name(self) -> None:
        """

        :return:
        Тестування def fullname(self) класу Employee
        """
        for good_item0 in self.good_str:
            for good_item1 in self.good_str:
                self.instance = sm.Employee(good_item0, good_item1, "Dev")
                self.assertEqual(self.instance.fullname, (good_item0.strip(), good_item1.strip()))

    def test_str_magic_method(self) -> None:
        """

        :return:
        Тестування def __str__(self) класу Employee
        """
        for good_item0 in self.good_str:
            for good_item1 in self.good_str:
                self.instance = sm.Employee(good_item0, good_item1, "Dev")
                self.assertEqual(self.instance.__str__(), (good_item0.strip() + ' ' + good_item1.strip()))

    def test_take_holiday(self) -> None:
        """

        :return:
        Тестування вибору відпустки тривалістю за значенням по замовченню.
        Значення по замовченню sm.Param.HLD_MIN_DAY.value
        У тесті здійснюємо 5 запитів, очікуємо, що залишок відпустки буде дорівнбвати нулю.
        """

        self.instance = sm.Employee(self.good_str[0], self.good_str[1], "Dev")
        for days in range(0, 5):
            before_change = self.instance.vacation_days
            self.instance.taking_holiday()
            self.assertEqual(before_change - sm.Param.HLD_MIN_DAY,
                             self.instance.vacation_days)

    def test_holiday_numdays(self) -> None:
        """
        :return:
        Тестування запиту на відпустку тривалість понад встановлений ліміт.
        Ліміт відпустки задається параметром sm.Param.VCTN_DAYS_INI.
        Тестуємо запит на відпустки в інтервалі [sm.Param.VCTN_DAYS_INI+1;
        sm.Param.VCTN_DAYS_INI+24].
        Очікуємо assertRaises(ValueError)
        """
        for days in range(sm.Param.VCTN_DAYS_INI + 1, sm.Param.VCTN_DAYS_INI + 25):
            self.instance = sm.Employee(self.good_str[0], self.good_str[1], "Dev")
            with self.assertRaises(ValueError):
                self.instance.taking_holiday(days)

    def test_take_holiday_min(self) -> None:
        """
        :return:
        тестування мінімально можливої тривалості відпустки.
        Мінімально можлива тривалість відпустки задається параметром sm.Param.HLD_MIN_DAY.
        Тестуємо запит на відпустки в інтервалі [-1;sm.Param.HLD_MIN_DAY-1].
        Очікуємо assertRaises(ValueError)
        """

        for days in range(-1, sm.Param.HLD_MIN_DAY):
            self.instance = sm.Employee(self.good_str[0], self.good_str[1], "Dev")
            with self.assertRaises(ValueError):
                self.instance.taking_holiday(days)

    def test_take_holiday_rand(self) -> None:

        """

        :return:
        Тестування отримання відпустки тривалістю від мінімально можливої, що визначається
        параметром sm.Param.HLD_MIN_DAY, до випадкового числа не більше 50.
        Очікуємо assertRaises(ValueError) у випадку коли запитуємо більше днів ніж залишок та
        сталу суму отриманих днів та залишку, яка повинна дорівнювати параметру
        sm.Param.VCTN_DAYS_INI
        """
        sum_days = 0
        self.instance = sm.Employee(self.good_str[0], self.good_str[1], "Dev")
        for i in range(50):
            days = random.randint(sm.Param.HLD_MIN_DAY, 50)
            if days > self.instance.vacation_days:
                with self.assertRaises(ValueError):
                    self.instance.taking_holiday(days)
            else:
                self.instance.taking_holiday(days)
                sum_days += days
                self.assertEqual(sm.Param.VCTN_DAYS_INI,
                                 self.instance.vacation_days + sum_days)

    def testing_payout(self) -> None:
        """

        :return:
         Тестування отримання відпустки тривалістю від 1 до випадкового числа не більше 50.
        Очікуємо assertRaises(ValueError) у випадку коли запитуємо більше днів ніж залишок та
        сталу суму отриманих днів та залишку, яка повинна дорівнювати параметру
        sm.Param.VCTN_DAYS_INI
        """
        sum_days = 0
        self.instance = sm.Employee(self.good_str[0], self.good_str[1], "Dev")
        for i in range(50):
            days = random.randint(-5, 50)
            if days > self.instance.vacation_days or days < 1:
                with self.assertRaises(ValueError):
                    self.instance.taking_payout(days)
            else:
                self.instance.taking_payout(days)
                sum_days += days
                self.assertEqual(sm.Param.VCTN_DAYS_INI,
                                 self.instance.vacation_days + sum_days)

    def test_logging_taking_payout(self) -> None:
        """

        :return:
        Тестування логінга метода taking_payout() класу Employee
        """
        # тестування повідомлень при штатному отриманні компенсації за дні відпустки
        for day in range(1, 25):
            self.instance = sm.Employee(self.good_str[0], self.good_str[1], "Dev")
            with self.assertLogs(LogParam.NAME_LOGGER.value, level='INFO') as cm:
                self.instance.taking_payout(day)
            self.assertEqual(cm.output, [f'INFO:{LogParam.NAME_LOGGER.value}:Taking a payout {day}. Remaining vacation '
                                         f'days: {self.instance.vacation_days}'])

    def test_logging_taking_holiday(self) -> None:
        """

        :return:
        Тестування логінга метода taking_holiday() класу Employee
        """
        for day in range(Param.HLD_MIN_DAY, 25):
            self.instance = sm.Employee(self.good_str[0], self.good_str[1], "Dev")
            with self.assertLogs(LogParam.NAME_LOGGER.value, level='INFO') as cm:
                self.instance.taking_holiday(day)
            self.assertEqual(cm.output,
                             [f'INFO:{LogParam.NAME_LOGGER.value}:Taking a holiday {day}. Remaining vacation '
                              f'days: {self.instance.vacation_days}'])


class HourlyEmployee(unittest.TestCase):
    bad_str = ["", "Bond1", "1bond", "david@", "@david", "111", 1, 1.68]
    good_str = ["Bond", "David", "Dev", " Bond", " Bond ", "Bond "]

    def test_init(self):
        """

        :return:

        """

    def testing_log_work(self) -> None:
        """

        :return:
        Тестування методу  log_work() класу HourlyEmployee.
        """

        #  тестування штатної роботи метода log_work
        self.instance = sm.HourlyEmployee(self.good_str[0], self.good_str[1], "Dev")
        sum_hours = 0
        for hours in range(1, Param.HOURLY_RATE):
            if sum_hours + hours > Param.AMOUNT_LIMIT:
                with self.assertRaises(ValueError):
                    self.instance.log_work(hours)
            else:
                self.instance.log_work(hours)
                sum_hours += hours
                self.assertEqual(sum_hours, self.instance.amount)

    def testing_check_limit_log_work(self) -> None:
        """

        :return:
        Метод тестує логіку метода check_limit_log_work  класу HourlyEmployee.
        Параметров AMOUNT_LIMIT = 302 встановний ліміт годин, які максимально може
        відпрацювати працівників. Тест перевіряє ініціацію ексепшена у випадку перевищення
        такого ліміту.

        """
        self.instance = sm.HourlyEmployee(self.good_str[0], self.good_str[1], "Dev")
        sum_hours = 0
        for i in range(365):
            hours = random.randint(1, Param.HOURLY_RATE)
            if sum_hours + hours > Param.AMOUNT_LIMIT:
                with self.assertRaises(ValueError):
                    self.instance.log_work(hours)
            else:
                self.instance.log_work(hours)
                sum_hours += hours
                self.assertEqual(sum_hours, self.instance.amount)

    def testing_raises_log_work(self) -> None:
        """

        :return:
        Тестування методу log_work() класу HourlyEmployee. Очікується raises(ValueError) для
        значень менше 1 та більше 50.
        """
        self.instance = sm.HourlyEmployee(self.good_str[0], self.good_str[1], "Dev")
        sum_hours = 0
        for hours in [-1, 0, 51, 60, 99]:
            with self.assertRaises(ValueError):
                self.instance.log_work(hours)

    def testinf_logging_log_work(self) -> None:
        """

        :return:
        Тестування logging методу log_work() класу HourlyEmployee.
        """
        self.instance = sm.HourlyEmployee(self.good_str[0], self.good_str[1], "Dev")
        sum_hours = 0
        for hours in range(1, Param.HOURLY_RATE):
            if not sum_hours + hours > Param.AMOUNT_LIMIT:
                sum_hours += hours
                with self.assertLogs(LogParam.NAME_LOGGER.value, level='INFO') as cm:
                    self.instance.log_work(hours)
                self.assertEqual(cm.output, [
                    f"INFO:{LogParam.NAME_LOGGER.value}:Employee {self.instance.fullname} amount {hours}. Full amount {sum_hours}"])


class TestSalariedEmployee(unittest.TestCase):

    def test_init(self):
        self.instance = sm.SalariedEmployee("David", "Bond", "Dev", 1)
        self.assertEqual("David", self.instance.first_name)
        self.assertEqual("Bond", self.instance.last_name)
        self.assertEqual("Dev", self.instance.role)
        self.assertEqual(1, self.instance.vacation_days)
        self.instance = sm.Employee("David", "Bond", "Dev")
        # перевірки ініціалізації vacation_days по замовченню
        self.assertEqual(25, self.instance.vacation_days)

    def test_init_raises(self):

        for salary_value in [1.25, "test", "100", 0, Param.SALARY_LIMIT + 1]:
            with self.assertRaises(ValueError):
                self.instance = sm.SalariedEmployee("David", "Bond", "Dev", salary=salary_value)

    def test_validate_salary(self) -> None:
        """

        :return:
        Тестування методу validate_salary() класу SalariedEmployee.
        Атрибут salary класу SalariedEmployee повинен перебувати у діапазоні від 1 (включно) до
        Param.SALARY_LIMIT (включно). Також  атрибут salary класу SalariedEmployee повинен бути типу int.
        У випадку відповідності цим умовам метод повертає True, у протилежному випадку провертає False.

        """
        self.instance = sm.SalariedEmployee("Bond", "David", "Dev")

        bad_values = [1.25, "test", "100", 0, Param.SALARY_LIMIT + 1]
        # очікувана поведінка повернення False
        for item in bad_values:
            res = self.instance.validate_salary(item)
            self.assertEqual(res, False)

        # очікувана поведінка повернення True
        for values in range(1, Param.SALARY_LIMIT + 1):
            res = self.instance.validate_salary(values)
            self.assertEqual(res, True)


class TestRoles(unittest.TestCase):

    def test_next(self):
        # список, який містить повтори ролей
        roles_str = ['CEO', "manager", " dev", 'CEO', " manager ", "dev"]
        # список, який містить лише унікальні ролі
        res_list = ['CEO', "manager", "dev"]
        roles = sm.Roles()

        # додаємо лише унікальні ролі
        for i in res_list:
            roles.add_role(i)

        for idx, item in enumerate(roles):
            self.assertEqual(res_list[idx], item)


    def test_add_roles(self):
        # список, який містить повтори ролей
        roles_str = ['CEO', "manager", " dev", 'CEO', " manager ", "dev"]
        # список, який містить лише унікальні ролі
        res_list = ['CEO', "manager", "dev"]
        roles = sm.Roles()

        # додаємо лише унікальні ролі
        for i in res_list:
            roles.add_role(i)

        # додаємо ролі, які місять дублікати. Очікуємо raises ValueError
        for i in roles_str:
            with self.assertRaises(ValueError):
                roles.add_role(i)
        pass

    def test_add_roles_warning_off(self):
        roles_str = ['CEO', "manager", " dev", 'CEO', " manager ", "dev"]
        res_list = ['CEO', "manager", "dev"]
        roles = sm.Roles()

        # створюємо еталонний список ролей
        for i in res_list:
            roles.add_role(i)

        # створюємо тестовий список ролей
        test_roles = sm.Roles()
        for i in roles_str:
                test_roles.add_role(i, warning= False)

        # порівнюємо тестовий список та контрольний список
        self.assertListEqual(roles.list_of_roles, test_roles.list_of_roles )



    def test_get_employee_by_role(self):
        company = sm.Company("one")
        company1 = sm.Company("too")
        company1.employees.append(sm.Employee("David", "Bond", "CEO", 1))
        company.employees.append(sm.Employee("David", "Bond", "Dev", 1))
        company.employees.append(sm.Employee("David", "Bond", "CEO", 1))
        company.employees.append(sm.Employee("David", "Bond", "manager", 1))
        res = company.get_employees_by_role("CEO")
        self.assertListEqual(res, company1.employees)


class TestCompany(unittest.TestCase):
    emp1 = sm.Employee("David", "Bond", "DEV", 1)
    emp2 = sm.Employee("David", "Bond", "CEO")
    emp3 = sm.HourlyEmployee("Jack", "Daniels", "CEO")
    emp4 = sm.HourlyEmployee("Chivas", "Regal", "CEO")
    emp5 = sm.SalariedEmployee("Black", "label", "HR")
    emp6 = sm.SalariedEmployee("Red", "label", "HR")
    test_set = [emp1, emp2, emp3, emp4, emp5, emp6]
    company = sm.Company("NFC")


    def test_validate_company_name(self):
        names = ["", " ", "@ddf", "???", ".", ".!@",1, 1.5]
        for name in names:
            with self.assertRaises(ValueError):
                company = sm.Company(name)

        names = [" AsD ", "asD, asd", "M&M"]
        for name in names:
            company = sm.Company(name)
            self.assertEqual(company.title, name.strip())

    def test_add_roles(self):
        test_set = ['deV', 'DEV', 'CEO', 'HR', 'hr', ' hr ']
        company = sm.Company('NFC')

        # тестування додавання посад без контролю дублікатів, передається строка
        for item in test_set:
            company.add_roles(item, warning=False)

        # тестування додавання посад з контролем дублікатів, передається строка
        company = sm.Company('NFC')
        company.add_roles('DEV', 'CEO', 'HR', warning=False)
        test_set = ['DEV', 'CEO', 'HR']
        for item in test_set:
            with self.assertRaises(ValueError):
                company.add_roles(item, warning=True)

        # тестування додавання посад без контролю дублікатів, передається екземпляр Role
            for item in test_set:
                company.add_roles(sm.Role(item), warning=False)

        # тестування додавання посад з контролем дублікатів, передається екземпляр Role
            company = sm.Company('NFC')
            company.add_roles('DEV', 'CEO', 'HR', warning=False)
            test_set = ['DEV', 'CEO', 'HR']
            for item in test_set:
                with self.assertRaises(ValueError):
                    company.add_roles(sm.Role(item), warning=True)

        # тестування додавання посад з контролем дублікатів, передається екземпляр Roles
        company = sm.Company('NFC')
        test_set = ['DEV', 'CEO', 'HR']
        inst_roles=sm.Roles()

        # створюємо тестовий набір посад в компанії
        for item in test_set:
            inst_roles.add_role(sm.Role(item))
        company.add_roles(inst_roles)

        # додаємо дублікати. ValueError.
        with self.assertRaises(ValueError):
            company.add_roles(inst_roles, warning=True)

        # додаємо дублікати.
        company.add_roles(inst_roles, warning=False)

    def test_pay(self):
        company = sm.Company("NFC")
        company.add_roles('DEV', 'CEO', 'HR', warning=False)
        for item in self.test_set:
            company.add_employee(item)
        for item in company.employees:
            item.pay()

    def test_payall(self):
        """

        :return:
        тестування методу pay_all()
        """
        company = sm.Company("NFC")
        company.add_roles('DEV', 'CEO', 'HR', warning=False)
        for item in self.test_set:
            company.add_employee(item)
        company.pay_all()


    def test_validate_employees(self):

        self.assertEqual(self.company.validate_employees(self.test_set), True)
        self.assertEqual(self.company.validate_employees([]), True)
        self.assertEqual(self.company.validate_employees(None), True)

    def test_add_employee(self):

        if self.company.employees is not None:
            self.company.employees.clear()

        for item in self.test_set:
            self.company.add_employee(item)

        company1 = sm.Company("one")
        company1.add_employee(self.emp1, self.emp3, self.emp4, self.emp5, self.emp6)
        self.assertListEqual(self.company.employees, company1.employees)



