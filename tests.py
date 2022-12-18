import unittest
import system as sm


class CompanyTest(unittest.TestCase):
    """Testing Company class"""
    inst_employee_1 = sm.Employee('NameOne', 'SurnameOne', 'CEO', 5)
    inst_employee_2 = sm.Employee('NameThree', 'SurnameThree', 'dev', 10)
    inst_employee_3 = sm.Employee('NameThree', 'SurnameThree', 'manager', 15)
    inst_employee_list = [inst_employee_1, inst_employee_2, inst_employee_3]

    def setUp(self):
        self.instance = sm.Company("5 company", self.inst_employee_list)

    def test_init(self):
        self.assertEquals("5 company", self.instance.title)
        self.assertEquals(self.inst_employee_list, self.instance.employees)

    def test_validate(self):
        self.assertEquals(self.instance.validate(
            "5 company", self.inst_employee_list), True)


