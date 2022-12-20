import unittest

import system


class EmsTestCase(unittest.TestCase):
    """Represents test cases"""

    def setUp(self) -> None:
        self.person_1 = system.Employee('Ivan', 'Green', 'dev', 5)
        self.person_2 = system.Employee('Victor', 'Papvik', 'CEO', 1)
        self.person_3 = system.Employee('Clint', 'Eastwood', 'manager', 0)
        self.person_4 = system.Employee('Sergiy', 'Zhyla', 'dev', 4)
        self.he_ceo = system.HourlyEmployee('Ibrahim', 'Forester', 'CEO')

    def test_initializer_employee(self):
        "This test case verifies initialization of Employee class instance."

        self.assertEqual('Ivan', self.person_1.first_name)
        self.assertEqual('Green', self.person_1.last_name)
        self.assertEqual('dev', self.person_1.role)
        self.assertEqual(5, self.person_1.vacation_days)

    def test_fullname(self):
        """This test case verifies 'fullname' method of Employee class"""

        self.assertEqual('Ivan Green', self.person_1.fullname)
