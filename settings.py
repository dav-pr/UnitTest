"""
Settings for advanced employee management system
"""
import enum
print(enum.__file__)


class Param(enum.IntEnum):
    VCTN_DAYS_INI = 25
    HLD_MIN_DAY = 5
    HOURLY_RATE = 50
    AMOUNT_LIMIT = 302


class LogParam(enum.Enum):
    NAME_LOGGER = "AEMS"
