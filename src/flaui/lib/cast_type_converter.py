from typing import Dict, List, Any


class TypeConverter:

    @staticmethod
    def cast_to_py_list(raw) -> List[Any]:
        return list(map(lambda x: x, raw))

    @staticmethod
    def cast_to_py_dict(raw) -> Dict[Any, Any]:
        return {_.Key: _.Value for _ in raw.GetEnumerator()}
