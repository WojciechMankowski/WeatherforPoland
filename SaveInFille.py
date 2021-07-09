import datetime
from os import path
from typing import Union, Any
from dataclasses import dataclass
import sqlite3

@dataclass
class SaveInDatabase:

    def Create(self, name_file: str)-> None:
        con = sqlite3.connect(f'Databese\{name_file}.db')
        cur = con.cursor()
        cur.execute(f'''CREATE TABLE Pogoda
                       (date text, Miasto text, Temperatura Integer, Opady Integer, Wilgodność Integer, Ciśnienie Integer)''')

    def CheckFile(self, name_file: str)-> bool:
        print("Sprawdzam czy istnieje plik")
        check =  path.exists(f'Databese\{name_file}.db')
        if check == False:
            self.Create(name_file)
            return False
        return check

    def save(self, *args) -> None:
        data_file = args[0]
        con = sqlite3.connect(f'Databese\{data_file}.db')
        cur = con.cursor()

        data = args[1]
        City = data[0]
        Date = data[1]
        Temperature = data[2]
        Humidity = data[3]
        Precipitation = data[4]
        Pressure = data[5]
        for index in range(len(City)):
            if Pressure[index] == None:
                Pressure[index] = 0
            query = f"INSERT INTO  Pogoda  VALUES (?, ?, ?, ?, ?, ?)"
            test =  Date[index],City[index],Temperature[index], Humidity[index], Precipitation[index], Pressure[index]
            cur.execute(query, test)
        con.commit()

    def CheckData(self, data_file: str, lastdate: datetime.datetime)-> bool:
        print("Sprawdzam ostatnią datę")
        data = []
        con = sqlite3.connect(f'Databese\{data_file}.db')
        cur = con.cursor()
        test = cur.execute('SELECT * FROM Pogoda ')
        for item in test:
            data.append(item[0])
        if len(data) == 0:
            LastDate = lastdate
        else:
            LastDate = data[-1]
        if LastDate == lastdate:
            return True
        else:
            return False