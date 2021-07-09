import datetime
import os
from typing import Optional, Match, Union
import pandas as pd
import sqlite3
import re
import matplotlib.pylab as plt
import scipy
import seaborn as sns

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
                                            minute=Minute) # type: ignore
        return datetime_object

class Analysis:
    def __init__(self):
        self.listDF = []
        _list = []
        self.data =[]
        self.df = pd.DataFrame(_list)
    # funkca odpowiedzialna za połączenie z odpowiednią bazą danych wraz z stowrzeniem DataFrame
    def readData(self, nameFile):
        fil = os.path.join(r"../", rf"Databese\{nameFile}")
        conn = sqlite3.connect(fil)
        df = pd.read_sql('SELECT * FROM Pogoda ', conn)
        __date = df["date"]
        for item in __date:
            date = Data().ObjectData(item)
            self.data.append(date)
        DATE = df["date"]
        ListData = []
        ListGodzina = []
        for item in DATE:
            item = str(item)
            ListData.append(item[:10])
            ListGodzina.append(item[11:])

        df["DATA"] = ListData
        df["Godzina"] = ListGodzina
        df["DATA"] = pd.to_datetime(df["DATA"])
        df["Godzina"] = pd.to_datetime(df["Godzina"])
        df["date"] = self.data
        self.listDF.append(df)
        self.data = []
    # funcka odpowiedzialna za połączenie wielu DF w jeden DataFrame
    def CombinationOfTables(self) -> pd.DataFrame:
        self.df = pd.concat(self.listDF)
        self.df = self.df.drop_duplicates()
        return self.df
    #  sprawdzenie czy nie ma braków w danych
    def MissingData(self)-> None:
        missingdata = (self.df.isnull().sum()).sum()
        if missingdata == 0:
            print("Wszystkie kolumny są zepełnione")
        else:
            print("Poniżej zestawienie kolumn i liczby braków")
            print(
                self.df.isnull().sum()
            )

#      funkcja odpowiedzialna za wyświetlenie postawowych informacji o danych
    def BasicInformation(self)-> None:
        stats = self.df.select_dtypes(['float', 'int']).describe()
        stats = stats.transpose()
        stats = stats[['count', 'std', 'min', '25%', '50%', '75%', 'max', 'mean']]
        print("Podstawowe statystyki")
        print(stats)
        print("Informacje o zbiorze")
        print(self.df.info())
#     statystyki dla określonej zmiennej
    def StatisticsForTheVariable(self, name_variable: str) -> None:
        df_variable = self.df[name_variable]
        plt.figure(figsize=(13, 7))
        sns.set(font_scale=1.4, style="whitegrid")
        sns.distplot(
            df_variable,
            kde=False,
            bins=30,
            color='#eb6c6a').set(title=f'Histogram - {name_variable}', xlabel=name_variable,
                                                                          ylabel='liczba obserwacji')
        plt.figure(figsize=(13, 7))
        sns.set(font_scale=1.4, style="whitegrid")
        sns.kdeplot(df_variable, shade=True, color='#eb6c6a').set(title=f'Wykres gęstości - {name_variable}', xlabel=name_variable,
                                                                 ylabel='')
        plt.figure(figsize=(13, 7))
        sns.boxplot(df_variable, color='#eb6c6a').set(title=f'Wykres pudełkowy - "{name_variable}"', xlabel=name_variable)

        if(scipy.stats.normaltest(df_variable)[1] < 0.05):
            print('Odrzucam hipotezę zerową i przyjmuję hipotezę alternatywną: zmienna nie pochodzi z rozkładu normalnego.')
        else:
            print('Przyjmuję hipotezę zerową. Zmienna pochodzi z rozkładu normalnego.')

        plt.show()
    def CategoricalVariables(self):
        df = self.df[['date', 'Miasto']]
        print(df.select_dtypes(exclude = ['float', 'int']).describe())
        print('Rozkład zmiennej data')
        print('-------------------------')
        print(df['date'].value_counts(normalize=True))
        print('Rozkład zmiennej Miasto')
        print('-------------------------')
        print(df['Miasto'].value_counts(normalize=True))
    def Corr(self) -> None:
        df = self.df
        corr_num = pd.DataFrame(scipy.stats.spearmanr(df.select_dtypes(include=['float', 'int']))[0],
                                columns=df.select_dtypes(include=['float', 'int']).columns,
                                index=df.select_dtypes(include=['float', 'int']).columns)

        plt.figure(figsize=(15, 6))
        sns.set(font_scale=1)
        sns.heatmap(corr_num.abs(), cmap="Reds", linewidths=.5).set(
            title='Heatmap-a współczynnika korelacji rang Spearmana')
        plt.show()
    def DataPreparation(self):
        df = self.df.drop(['date', 'Miasto','DATA', 'Godzina'], axis=1)
        wines =df
        results = []
        for feature in wines.columns:
            alpha = 0.05
            p_value = scipy.stats.normaltest(wines[feature])[1]
            results.append([feature, p_value])
            if (p_value < alpha):
                print(
                    'Dla zmiennej \'' + feature + '\' odrzucam hipotezę zerową. Zmienna NIE POCHODZI z rozkładu normalnego. P-value:',
                    p_value)
            else:
                print(
                    'Dla zmiennej \'' + feature + '\' nie wykryto podstaw do odrzucenia hipitezy zerowej. Zmienna POCHODZI z rozkładu normalnego. P-value:',
                    p_value)
            podsumowanie = pd.DataFrame(results)
            podsumowanie.columns = ['nazwa_zmiennej', 'p_value']
            podsumowanie.set_index('nazwa_zmiennej', inplace=True)
            podsumowanie.sort_values('p_value', ascending=False, inplace=True)
            print(podsumowanie)

def run_analysis():
    #  zadeklorowanie klasy związanej z analizą
    analysis = Analysis()
    #  stowrzenie listy z plikami
    Lista_file = list(os.listdir('../Databese'))
    # pętla odpowiedzialna za utworzenie tabeli z DataFrame
    for nameFile in Lista_file:
        analysis.readData(nameFile)
    #  połączenie tabeli z DataFrame w jedną zmienną
    analysis.CombinationOfTables()
    Gdansk = analysis.df[analysis.df["Miasto"]=="Gdańsk"]
    print(Gdansk[["date", "Temperatura"]])
    Gdansk = Gdansk[["date", "Temperatura"]]
    plt.plot(Gdansk['date'], Gdansk['Temperatura'])
    plt.show()
    # analysis.DataPreparation()

run_analysis()