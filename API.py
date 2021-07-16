from dataclasses import dataclass
from typing import Union
from requests import get
from json import loads
from Exception import DatabaseConnectionStatusException
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
        if status != 200:
            raise DatabaseConnectionStatusException()
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


if __name__ == '__main__':
    APIConnection("https://danepubliczne.imgw.pl/api/data/synop").Connection()
