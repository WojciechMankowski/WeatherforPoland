from zoneinfo import ZoneInfo
from typing import Optional, Union, Match
import datetime
import re

class Data:
    def ObjectData(self, data_str: str) -> datetime.datetime:
        Year_re = re.compile(r'(\d{4})')
        M_re = re.compile(r'-(\d{2})')
        Hour_re = re.compile(r'(\d+):')
        Year: Optional[Match[str]] = Year_re.match(data_str)
        Year2: str= Year.group() #type: ignore
        Year_int: Union[int, str] = int(Year2)
        M: int = int(M_re.findall(data_str)[0])
        Day: int = int(M_re.findall(data_str)[1])
        Hour: int = int(Hour_re.findall(data_str)[0])
        Minute: int = 00
        datetime_object = datetime.datetime(year=Year_int, month=M, day=Day, hour=Hour,
                                            minute=Minute, tzinfo=ZoneInfo('Europe/Warsaw')) # type: ignore
        return datetime_object