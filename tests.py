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
        self.instance = sm.Employee("David", "Bond", "Dev", 1)
        self.assertEqual("David", self.instance.first_name)
        self.assertEqual("Bond", self.instance.last_name)
        self.assertEqual("Dev", self.instance.role)
        self.assertEqual(1, self.instance.vacation_days)
        self.instance = sm.Employee("David", "Bond", "Dev")
        # перевірки ініціалізації vacation_days по замовченню
        self.assertEqual(25, self.instance.vacation_days)

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
            self.assertEqual(cm.output, [f'INFO:{LogParam.NAME_LOGGER.value}:Taking a holiday {day}. Remaining vacation '
                                         f'days: {self.instance.vacation_days}'])


class HourlyEmployee(unittest.TestCase):
    bad_str = ["", "Bond1", "1bond", "david@", "@david", "111", 1, 1.68]
    good_str = ["Bond", "David", "Dev", " Bond", " Bond ", "Bond "]

    def testing_log_work(self) -> None:
        """

        :return:
        Тестування методу  log_work() класу HourlyEmployee.
        """

        #  тестування штатної роботи метода log_work
        self.instance = sm.HourlyEmployee(self.good_str[0], self.good_str[1], "Dev")
        sum_hours = 0
        for hours in range(1, Param.HOURLY_RATE):
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
            sum_hours += hours
            with self.assertLogs(LogParam.NAME_LOGGER.value, level='INFO') as cm:
                self.instance.log_work(hours)
            self.assertEqual(cm.output, [f"INFO:{LogParam.NAME_LOGGER.value}:Employee {self.instance.fullname} amount {hours}. Full amount {sum_hours}"])




