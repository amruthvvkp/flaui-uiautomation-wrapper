"""This module contains unit tests to the collections module."""
from flaui.lib.collections import TypeCast


class TestTypeCast:
    """Tests the TypeCast class."""
    def test_py_list(self):
        """
        Test the conversion of a C# List object to a Python list.
        """
        from System.Collections.Generic import List  # pyright: ignore

        test_object = List[str]()  # This is a C# List object
        test_dict = {0: "A", 1: "B", 2: "C"}

        for v in test_dict.values():
            test_object.Add(v)

        converted = TypeCast.py_list(test_object)

        assert len(test_object) == len(test_dict)
        assert len(converted) == len(test_dict)

        for k, v in test_dict.items():
            assert converted[k] == v

    def test_py_dict(self):
        """
        Test the conversion of a C# Dictionary object to a Python dictionary.
        """
        from System.Collections.Generic import Dictionary  # pyright: ignore
        from System.Collections.Generic import IDictionary  # pyright: ignore

        test_object = IDictionary[str, str](Dictionary[str, str]())
        test_dict = {"0": "A", "1": "B", "2": "C"}

        for k, v in test_dict.items():
            test_object[k] = v

        converted = TypeCast.py_dict(test_object)

        assert len(test_object) == len(test_dict)
        assert len(converted) == len(test_dict)

        for k, v in test_dict.items():
            assert converted[k] == v
