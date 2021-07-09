import os
import datetime

import pandas as pd
from Chart import Diagrams
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

class InitialAnalysis:
    def __init__(self):
        _list = []
        self.listDF = []
        self.df: pd.DataFrame = pd.DataFrame(_list)
    def creatingfiles(self, namefile: str) -> pd.DataFrame:
        fille = f"Folder z plikami z csv/{namefile}.csv"
        # fille = f"Folder z plikami z csv/2021_07_06.csv"
        self.nameFile = pd.read_csv(fille,encoding='Windows-1252')
        self.nameFile.columns = ["Miasto", "Data i godzina", "Temperatura", "Opady", "Wilgodność"]
        return self.nameFile
    def DisplayingTheHeader(self, dane: pd.DataFrame) -> None:
        print(dane.head())
        print(dane.info())
    def CombinationOfTables(self, dane: pd.DataFrame) -> pd.DataFrame:
        df = self.df
        self.AddToList(dane)
        df = pd.concat(self.listDF)
        df["Data i godzina"] = pd.to_datetime(df["Data i godzina"])
        self.df = df

        return  self.df

    def AddToList(self, dane: pd.DataFrame)-> None:
        self.listDF.append(dane)

    def CheckData(self):
        col = ['Miasto', 'Data i godzina', 'Temperatura', 'Opady', 'Wilgodność']
        self.df.columns = col
        check = self.df.duplicated().sum()
        self.df.drop_duplicates()

    def BasicStatistics(self):
        statistics = self.df.describe()
        print(statistics)

class Timeseries:
    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df
        # print(self.df[['Data i godzina',"Miasto","Temperatura"]])
        # self.df = self.df.set_index('Data i godzina')
        print(self.df.columns)
        mean_time = self.df.groupby("Miasto").mean()
        # mean_time["Data"] = self.df.index
        #
        # .resample('W').mean()
        print(mean_time)
def run():
    analysis = InitialAnalysis()
    Lista_file = list(os.listdir('../Folder z plikami z csv'))
    Dane = ""
    for row in Lista_file:
        name_file = row[0:10]
        dane = analysis.creatingfiles(name_file)
        Dane = analysis.CombinationOfTables(dane)

    timclass = Timeseries(Dane)
    # analysis.CheckData()
    # analysis.BasicStatistics()
    # analysis.DisplayingTheHeader(Dane)

    chart = Diagrams(Dane)
    chart.GroupingOfData("Temperatura")
    chart.GroupingOfData("Opady")
    chart.GroupingOfData("Wilgodność")
    # chart.TemperatureChartForCities()
    # chart.BoxPlot(Dane)
    # chart.ConnectingVariables()
if __name__ == '__main__':
    run()