"""This module contains collections which can effective handle data transition between C# and Python."""

from datetime import date
from typing import Any, Dict, List

import arrow
from System import (
    DateTime as CSDateTime,
    TimeSpan,  # pyright: ignore
)


class TypeCast:
    """A class that provides methods to convert C# objects to Python objects"""

    @staticmethod
    def py_list(raw: Any) -> List[Any]:
        """Converts C# Lists to Python lists

        :param raw: Raw C# list object
        :return: Converted Python List object
        """
        return raw if isinstance(raw, list) else list(map(lambda x: x, raw))

    @staticmethod
    def py_dict(raw: Any) -> Dict[Any, Any]:
        """Converts C# Dict to Python Dict

        :param raw: Raw C# Dict object
        :return: Converted Python Dict object
        """
        return raw if isinstance(raw, dict) else {_.Key: _.Value for _ in raw.GetEnumerator()}

    @staticmethod
    def cs_timespan(value: int) -> Any:
        """Converts a Python time milliseconds value to C# TimeSpan object

        :param value: Time in milliseconds
        :return: TimeSpan object from C# System
        """
        if value is None:
            return None

        return TimeSpan.FromMilliseconds(value)

    @staticmethod
    def cs_datetime(date: date):
        """Parses Python date as C# Datetime object

        :param date: Python date
        """
        return CSDateTime.Parse(arrow.get(date).strftime("%Y-%m-%d"))
