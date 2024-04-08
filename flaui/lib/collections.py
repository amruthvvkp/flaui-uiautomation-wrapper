"""This module contains the TypeCast class which is used to convert C# objects to Python objects."""

from typing import Any, Dict, List


class TypeCast:
    """TypeCast class to convert C# objects to Python objects."""

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
