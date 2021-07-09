import matplotlib.pyplot as plt
import plotly.express as px
import  seaborn as sns
import pandas as pd

class Diagrams:

    def __init__(self, dane: pd.DataFrame) -> None:
        self.df = dane
        self.CITY = [
            'Białystok', 'Bielsko Biała', 'Chojnice', 'Częstochowa', 'Elbląg',
            'Gdańsk', 'Gorzów', 'Hel', 'Jelenia Góra', 'Kalisz', 'Kasprowy Wierch',
            'Katowice', 'Kielce', 'Koszalin', 'Kozienice', 'Koło', 'Kołobrzeg',
            'Kraków', 'Krosno', 'Kłodzko', 'Kętrzyn', 'Legnica', 'Lesko', 'Leszno',
            'Lublin', 'Lębork', 'Mikołajki', 'Mława', 'Nowy Sącz',
            'Olsztyn', 'Opole', 'Ostrołęka', 'Piła', 'Platforma', 'Poznań',
            'Przemyśl', 'Płock', 'Racibórz', 'Resko', 'Rzeszów', 'Sandomierz',
            'Siedlce', 'Sulejów', 'Suwałki', 'Szczecin', 'Szczecinek', 'Słubice',
            'Tarnów', 'Terespol', 'Toruń', 'Ustka', 'Warszawa', 'Wieluń', 'Wrocław',
            'Włodawa', 'Zakopane', 'Zamość', 'Zielona Góra', 'Łeba',
            'Łódź', 'Mikołajki', 'Świnoujście',
        ]
        print(type(self.CITY))
        print(len(self.CITY))
        city = list(set(self.CITY))
        print(len(city))

        self.DF = []
    def GroupingOfData(self, ColumnNname: str) -> None:
        tabel = [f'{ColumnNname}', "Miasto"]
        df = self.df[tabel]
        df = df.groupby("Miasto").mean()
        df.index = self.CITY
        self.DF.append(df)
    def ConnectingVariables(self) -> pd.DataFrame:
        # df = self.df[["Data i godzina", "Miasto"]]
        df = self.df["Data i godzina"]
        data = []
        for row in df:
            data.append(row)
        data.sort()
        # data = list(set(data))
        DF = pd.DataFrame(data)
        print(DF.shape)
        # print(DF)
        return df

    def TemperatureChartForCities(self):
        temperatura = self.df.groupby("Miasto").mean()
        temperatura = temperatura[["Temperatura", "Opady"]]
        temperatura.index = self.CITY
        sns.set_context('paper')
        sns.relplot(data=temperatura,
                    x="Opady",
                    y="Temperatura",
                    aspect=2.5,
                    # kind='line',
                    hue=temperatura.index,
                    kind = "scatter",
                    )

        plt.show()

    def BoxPlot(self, dane):
        pass