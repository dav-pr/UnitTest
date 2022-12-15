
import unittest
import system

class EmployeeTest(unittest.TestCase):
    def setUp(self) -> None:
        self.instance = system.Employee("David", "Bond", "Dev", 999)

    def test_ini(self):
        self.assertEqual("David", self.instance.first_name)
        self.assertEqual("Bond", self.instance.last_name)
        self.assertEqual("Dev", self.instance.role)
        self.assertEqual(999,self.instance.vacation_days)


