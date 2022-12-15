
import unittest
import system

class EmployeeTest(unittest.TestCase):
    def setUp(self) -> None:
        self.instance = system.Employee("David", "Bond", "Dev", 999)

    def test_ini(self):
        self.assertEquals("David", self.instance.first_name)
        self.assertEquals("Bond", self.instance.last_name)
        self.assertEquals("Dev", self.instance.role)
        self.assertEquals(999,self.instance.vacation_days)


