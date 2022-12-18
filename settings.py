"""
Settings for advanced employee management system
"""
import enum


class Param(enum.IntEnum):
    VCTN_DAYS_INI = 25
    HLD_MIN_DAY = 5
    HOURLY_RATE = 50
    AMOUNT_LIMIT = 302
    SALARY_LIMIT = 10_000


class LogParam(enum.Enum):
    NAME_LOGGER = "AEMS"
