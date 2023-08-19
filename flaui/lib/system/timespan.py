"""This module provides a wrapper for the TimeSpan class from the object <class 'System.TimeSpan'> from the module - System."""
# Still a work in progress

from pydantic import BaseModel
from pydantic import ConfigDict
from System import TimeSpan as CSTimeSpan  # pyright: ignore

class TimeSpan(BaseModel):
    """
    A wrapper class for using the Timespan class from .NET System namespace.
    """
    model_config: ConfigDict = ConfigDict(arbitrary_types_allowed=True)

    cs_object: CSTimeSpan = CSTimeSpan()

    @property
    def total_milliseconds(self):
        """
        Gets the value of the current System.TimeSpan structure expressed in whole and fractional milliseconds.

        :return: The total number of milliseconds represented by this instance.
        """
        return self.cs_object.TotalMilliseconds

    @property
    def total_hours(self):
        """
        Gets the value of the current System.TimeSpan structure expressed in whole and fractional hours.

        :return: The total number of hours represented by this instance.
        """
        return self.cs_object.TotalHours
