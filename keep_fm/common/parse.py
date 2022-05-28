from datetime import datetime, date
from typing import Optional, Union, List, cast


def get_date_or_none(d: Union[None, str, List[str]]) -> Optional[date]:
    if d is None:
        return None

    if type(d) is list:
        if len(d) == 1:
            d = d[0]
        else:
            raise ValueError("If value is a list, then it has to have only one element")

    if d == "":
        return None
    return datetime.strptime(cast(str, d), "%Y-%m-%d").date()


def get_str_or_none(v: Union[None, str, List[str]]) -> Optional[str]:
    if v is None:
        return None

    if type(v) is list:
        if len(v) == 1:
            v = v[0]
        else:
            raise ValueError("If value is a list, then it has to have only one element")

    if v == "":
        return None
    return cast(str, v)


def get_int_or_none(v: Union[None, str, List[str]]) -> Optional[int]:
    v = get_str_or_none(v)

    if v is not None:
        try:
            return int(v)
        except ValueError:
            return None
    return None
