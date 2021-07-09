from dataclasses import dataclass
from typing import Union
from requests import get
from json import loads
from CreateANewDate import Data
import datetime

@dataclass
class APIConnection:
    City: list[str]
    Date: list[datetime.datetime]
    Temperature: list[str]
    Humidity: list[str]
    Precipitation: list[str]
    Pressure: list[str]
    def __init__(self, URL: str) -> None:
        self.url = URL
        self.City= []
        self.Date= []
        self.Temperature = []
        self.Humidity  = []
        self.Precipitation = []
        self.Pressure = []
    def Connection(self) -> list[dict[str, str]]:
        responsy = get(self.url)
        status = responsy.status_code
        print(f"Status połączenia: {status}")
        data =loads(responsy.text)
        return data
    def SelectionOfItems(self, data: list[dict[str, str]]):
        for row in data:
            data_str = f'{row["data_pomiaru"]} {row["godzina_pomiaru"]}:00' # type: ignore
            data = Data().ObjectData(data_str) # type: ignore
            # print(type(data))
            # data = int(data)
            # data = data.toordinal()
            self.Date.append(data)  # type: ignore
            temperatura = row['temperatura']  # type: ignore
            self.Temperature.append(temperatura)
            humidity = row['wilgotnosc_wzgledna'] # type: ignore
            self.Humidity.append(humidity)
            precipitation = row['suma_opadu'] # type: ignore
            self.Precipitation.append(precipitation)
            pressure = row['cisnienie'] # type: ignore
            self.Pressure.append(pressure)
            city = row['stacja'] # type: ignore
            self.City.append(city)
    def CreateADictionaryForWriting(self) -> list[Union[list[str], list[datetime.datetime]]]:

        length = len(self.City)
        Weather: list[Union[list[str], list[datetime.datetime]]] = []
        Weather.append(self.City)
        Weather.append(self.Date)
        Weather.append(self.Temperature)
        Weather.append(self.Humidity)
        Weather.append(self.Precipitation)
        Weather.append(self.Pressure)

        return Weather

    # def ObjectData(self, data_str: str):
    #     Year_re = re.compile(r'(\d{4})')
    #     M_re = re.compile(r'-(\d{2})')
    #     Hour_re = re.compile(r'(\d+):')
    #     Minute_re = re.compile(r':(\d{2})')
    #     Year= Year_re.match(data_str) # type: ignore
    #     Year2= Year.group() # type: ignore
    #     Year = int(Year2) # type: ignore
    #     M = int(M_re.findall(data_str)[0])
    #     Day = int(M_re.findall(data_str)[1])
    #     Hour = int(Hour_re.findall(data_str)[0])
    #     Minute = int(Minute_re.findall(data_str)[0])
    #     datetime_object = datetime.datetime(year=Year, month=M, day=Day, hour=Hour,
    #                                         minute=Minute, tzinfo=ZoneInfo('Europe/Warsaw'))
    #     return datetime_object
