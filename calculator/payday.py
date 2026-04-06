import calendar
from abc import ABC, abstractmethod
from datetime import date, timedelta


class PaydayStrategy(ABC):
    """Determines when payday falls for a given month."""

    @property
    @abstractmethod
    def key(self) -> str:
        """Unique identifier used in query params."""

    @property
    @abstractmethod
    def label(self) -> str:
        """Human-readable name shown in the UI."""

    @abstractmethod
    def get_payday(self, year: int, month: int) -> date:
        """Return the payday date for the given year/month."""


class SecondLastWorkingDay(PaydayStrategy):
    """Payday is the second-last Mon–Fri of the month."""

    key = "second_last_working_day"
    label = "2nd-last working day"

    def get_payday(self, year: int, month: int) -> date:
        day = date(year, month, calendar.monthrange(year, month)[1])
        count = 0
        while True:
            if day.weekday() < 5:
                count += 1
                if count == 2:
                    return day
            day -= timedelta(days=1)


class LastWorkingDay(PaydayStrategy):
    """Payday is the last Mon–Fri of the month."""

    key = "last_working_day"
    label = "Last working day"

    def get_payday(self, year: int, month: int) -> date:
        day = date(year, month, calendar.monthrange(year, month)[1])
        while day.weekday() >= 5:
            day -= timedelta(days=1)
        return day


class FixedDay(PaydayStrategy):
    """Payday is a fixed day of the month (e.g. the 25th).

    If the day falls on a weekend, rolls back to the preceding Friday.
    """

    def __init__(self, day_of_month: int = 25):
        self._day = day_of_month

    @property
    def key(self) -> str:
        return f"fixed_{self._day}"

    @property
    def label(self) -> str:
        return f"Fixed day {self._day}"

    def get_payday(self, year: int, month: int) -> date:
        _, last_dom = calendar.monthrange(year, month)
        d = date(year, month, min(self._day, last_dom))
        while d.weekday() >= 5:
            d -= timedelta(days=1)
        return d


STRATEGIES = [
    SecondLastWorkingDay(),
    LastWorkingDay(),
    FixedDay(25),
    FixedDay(1),
]

STRATEGY_MAP = {s.key: s for s in STRATEGIES}
DEFAULT_STRATEGY = STRATEGIES[0]


def get_strategy(key: str | None) -> PaydayStrategy:
    """Look up a strategy by key, falling back to the default."""
    return STRATEGY_MAP.get(key, DEFAULT_STRATEGY)
