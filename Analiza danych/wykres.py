class Chart:
    def __init__(self):
        super(Chart, self).__init__()
    def chartHext(self, df, x: str, y: str):
        x = df[x]
        y = df[y]
        sns.jointplot(x=x, y=y, kind="hex", color="#4CB391")
        plt.show()

    def Corr(self, df):
        df = df[['Temperatura', 'Opady', 'Wilgodność', 'Ciśnienie']]
        corr = df.corr()
        mask = np.triu(np.ones_like(corr, dtype=bool))

        # Set up the matplotlib figure
        f, ax = plt.subplots(figsize=(11, 9))
        cmap = sns.diverging_palette(230, 20, as_cmap=True)
        sns.heatmap(corr, mask=mask, cmap=cmap, vmax=.3, center=0,
                    square=True, linewidths=.8, cbar_kws={"shrink": .5})
        plt.show()
    def Relplot(self, df, x, y, city):
        df = df[(df["Miasto"] == city[0]) | (df["Miasto"] == city[1])]
        sns.relplot(x=x, y=y, hue="Miasto", size=y,
                    sizes=(0, 250),
                    alpha=.5, palette="muted",
                    height=6, data=df, )
        sns.relplot(x=x, y=y, hue="Miasto",
                    alpha=.5, palette="muted", kind='line', aspect=2.5,
                    height=6, data=df, )

    def Boxplot(self, df, x, y, city):
        df = df[(df["Miasto"] == city[0]) | (df["Miasto"] == city[1])]
        sns.catplot(x=x,
                    y=y,
                    data=df,
                    aspect=2.5,
                    kind='box',
                    hue='Miasto'
                    )
        plt.show()