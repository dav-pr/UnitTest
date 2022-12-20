import logging
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.INFO)


# noinspection PyTypeChecker
@dataclass
class Employee:
    """Basic employee representation"""

    first_name: str
    last_name: str
    role: str
    vacation_days: int = 25

    @property
    def fullname(self):
        """Return employe's full name"""

        return f'{self.first_name} {self.last_name}'

    def __str__(self) -> str:
        """Return a string version of an instance"""

        return self.fullname

    def take_payout_holiday(self):
        """Take a payout vacation"""

        if self.vacation_days < 5:
            msg = f"{self} have not enough vacation days. " \
                  f"Remaining days: %d. Requested: %d" % (self.vacation_days, 5)
            raise ValueError(msg)
        self.vacation_days -= 5
        msg = f"Taking a payout vacation. Remaining vacation days: %d " % (self.vacation_days)
        logger.info(msg)

    def take_single_holiday(self):
        """Take a single holiday"""

        if self.vacation_days < 1:
            msg = f"{self} have not enough vacation days. " \
                  f"Remaining days: %d. Requested: %d" % (self.vacation_days, 1)
            raise ValueError(msg)
        self.vacation_days -= 1
        msg = "Taking a single holiday. Remaining vacation days: %d " % (self.vacation_days)
        logger.info(msg)


# noinspection PyTypeChecker
@dataclass
class HourlyEmployee(Employee):
    """Represents employees who are paid on worked hours base"""

    amount: int = 0
    hourly_rate: int = 50

    def log_work(self, hours: int) -> None:
        """Log working hours"""

        self.amount += hours