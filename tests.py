
import unittest
import system

class EmployeeTest(unittest.TestCase):

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

        bad_str=["","Bond1", "1bond", "david@", "@david","111",1, 1.68]
        good_str=["Bond", "David", "Dev", " Bond", " Bond ", "Bond "]
        for good_item in good_str:
            for item in bad_str:
                with self.assertRaises(ValueError):
                    system.Employee(item, good_item, good_item, 1)

        for good_item0 in good_str:
            for good_item1 in good_str:
                for good_item2 in good_str:
                    instance = system.Employee(good_item0, good_item1, good_item2, 1)
                    self.assertEqual(good_item0.strip(), instance.first_name)
                    self.assertEqual(good_item1.strip(), instance.last_name)
                    self.assertEqual(good_item2.strip(), instance.role)




















