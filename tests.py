import random
import unittest
import system

class EmployeeTest(unittest.TestCase):
    bad_str = ["", "Bond1", "1bond", "david@", "@david", "111", 1, 1.68]
    good_str = ["Bond", "David", "Dev", " Bond", " Bond ", "Bond "]

    def test_ini(self):
        """
        :return:
        Тестування правильності ініціалізації параметров.
        Даний тест не виконує валідацію введених даний, а просто перевіряя правильність передачі даних при ініціалізації
        """
        self.instance = system.Employee("David", "Bond", "Dev", 1)
        self.assertEqual("David", self.instance.first_name)
        self.assertEqual("Bond", self.instance.last_name)
        self.assertEqual("Dev", self.instance.role)
        self.assertEqual(1,self.instance.vacation_days)
        self.instance = system.Employee("David", "Bond", "Dev")
        # перевірки ініціалізації vacation_days по замовченню
        self.assertEqual(25, self.instance.vacation_days)


    def test_validate(self):
        # тестування правильності введення кількості днів
        bad_days = [-1, 32, 99, 100]
        for i in bad_days:
            with self.assertRaises(ValueError):
                system.Employee("David", "Bond", "Dev", i)


        for i in range(1, 32):
            # памєятаємо, що 32 не включається
            self.instance=system.Employee("David", "Bond", "Dev", i)
            self.assertEqual(i, self.instance.vacation_days)

        # тестування спрацювання raise (ValueError)

        for good_item in self.good_str:
            for item in self.bad_str:
                with self.assertRaises(ValueError):
                    system.Employee(item, good_item, good_item, 1)

        for good_item0 in self.good_str:
            for good_item1 in self.good_str:
                for good_item2 in self.good_str:
                    instance = system.Employee(good_item0, good_item1, good_item2, 1)
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
                self.instance = system.Employee(good_item0, good_item1, "Dev")
                self.assertEqual(self.instance.fullname, (good_item0.strip(),good_item1.strip()))

    def test_str_magic_method(self) -> None:
        """

        :return:
        Тестування def __str__(self) класу Employee
        """
        for good_item0 in self.good_str:
            for good_item1 in self.good_str:
                self.instance = system.Employee(good_item0, good_item1, "Dev")
                self.assertEqual(self.instance.__str__(), (good_item0.strip()+' '+good_item1.strip()))

    def test_take_holiday(self) -> None:
        """

        :return:
        Тестування вибору відпустки тривалістю за значенням по замовченню.
        Значення по замовченню system.Param.HLD_MIN_DAY.value
        У тесті здійснюємо 5 запитів, очікуємо, що залишок відпустки буде дорівнбвати нулю.
        """

        self.instance = system.Employee(self.good_str[0], self.good_str[1], "Dev")
        for days in range(0,5):
            before_change = self.instance.vacation_days
            self.instance.taking_holiday()
            self.assertEqual(before_change - system.Param.HLD_MIN_DAY.value,
                             self.instance.vacation_days)

    def test_holiday_numdays(self) -> None:
        """
        :return:
        Тестування запиту на відпустку тривалість понад встановлений ліміт.
        Ліміт відпустки задається параметром system.Param.VCTN_DAYS_INI.
        Тестуємо запит на відпустки в інтервалі [system.Param.VCTN_DAYS_INI+1;
        system.Param.VCTN_DAYS_INI+24].
        Очікуємо assertRaises(ValueError)
        """
        for days in range(system.Param.VCTN_DAYS_INI.value+1,system.Param.VCTN_DAYS_INI.value+25):
            self.instance = system.Employee(self.good_str[0], self.good_str[1], "Dev")
            with self.assertRaises(ValueError):
                self.instance.taking_holiday(days)

    def test_take_holiday_min(self)-> None:
        """
        :return:
        тестування мінімально можливої тривалості відпустки.
        Мінімально можлива тривалість відпустки задається параметром system.Param.HLD_MIN_DAY.
        Тестуємо запит на відпустки в інтервалі [-1;system.Param.HLD_MIN_DAY-1].
        Очікуємо assertRaises(ValueError)
        """

        for days in range(-1, system.Param.HLD_MIN_DAY.value):
            self.instance = system.Employee(self.good_str[0], self.good_str[1], "Dev")
            with self.assertRaises(ValueError):
                self.instance.taking_holiday(days)

    def test_take_holiday_rand(self) -> None:

        """

        :return:
        Тестування отримання відпустки тривалістю від мінімально можливої, що визначається
        параметром system.Param.HLD_MIN_DAY, до випадкового числа не більше 50.
        Очікуємо assertRaises(ValueError) у випадку коли запитуємо більше днів ніж залишок та
        сталу суму отриманих днів та залишку, яка повинна дорівнювати параметру
        system.Param.VCTN_DAYS_INI
        """
        sum_days=0
        self.instance = system.Employee(self.good_str[0], self.good_str[1], "Dev")
        for i in range(50):
            days=random.randint(system.Param.HLD_MIN_DAY.value,50)
            if days>self.instance.vacation_days:
                with self.assertRaises(ValueError):
                    self.instance.taking_holiday(days)
            else:
                self.instance.taking_holiday(days)
                sum_days+=days
                self.assertEqual(system.Param.VCTN_DAYS_INI.value,
                                 self.instance.vacation_days+sum_days)

    def testing_payout(self) ->None:
        """

        :return:
         Тестування отримання відпустки тривалістю від 1 до випадкового числа не більше 50.
        Очікуємо assertRaises(ValueError) у випадку коли запитуємо більше днів ніж залишок та
        сталу суму отриманих днів та залишку, яка повинна дорівнювати параметру
        system.Param.VCTN_DAYS_INI
        """
        sum_days = 0
        self.instance = system.Employee(self.good_str[0], self.good_str[1], "Dev")
        for i in range(50):
            days = random.randint(-5, 50)
            if days > self.instance.vacation_days or  days < 1:
                with self.assertRaises(ValueError):
                    self.instance.taking_payout(days)
            else:
                self.instance.taking_payout(days)
                sum_days += days
                self.assertEqual(system.Param.VCTN_DAYS_INI.value,
                                 self.instance.vacation_days + sum_days)


































