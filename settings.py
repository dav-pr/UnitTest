"""
Settings for advanced employee management system
"""
import enum


class Param(enum.IntEnum):
    # початкове значення тривалості відпустки
    VCTN_DAYS_INI = 25
    # мінімальна тривалість відпустки
    HLD_MIN_DAY = 5
    # тривалість робочого тижня
    HOURLY_RATE = 50
    # максимальна тривалість робоичх годин у рік
    AMOUNT_LIMIT = 302
    # максимально можливий посадовий оклад
    SALARY_LIMIT = 10_000
    # посадовий оклад за замовченню
    SALARY_DEFAULT = 5_000



class LogParam(enum.Enum):
    # найменування логера
    NAME_LOGGER = "AEMS"
