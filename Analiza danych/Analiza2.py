import os
import pandas as pd
import sqlite3
import matplotlib.pylab as plt
import plotly.express as px
import statsmodels.api as sm
from sklearn import linear_model
import seaborn as sns
import numpy as np
from sklearn.linear_model import LinearRegression

fil = os.path.join(r"/", r"Databese\2021_07_07.db")
conn = sqlite3.connect(fil)
df = pd.read_sql('SELECT * FROM Pogoda ', conn)
df["date"] = pd.to_datetime(df["date"])
DATE = df["date"]
ListData = []
for item in DATE:
    item = str(item)
    ListData.append(item[:10])

df["DATA"] = ListData
# df["DATA"] = pd.to_datetime(df["DATA"])
# print(df["Opady"].min(), df["Opady"].max())
# print(df["Temperatura"].min(), df["Temperatura"].max())

# fig = px.scatter(df,
#         x="Opady", y="Temperatura", size="Temperatura",
#         color="Miasto",
#         hover_name="Miasto", log_x=True,
#         size_max=35, template="simple_white",
#         animation_frame="DATA", animation_group="Miasto",
#         range_x=[20,100], range_y=[10,35]
#         )
#

# fig.show()



# plt.scatter(X, y)
# plt.xlabel("Liczba opadów")
# plt.ylabel("Temperatura")

# plt.show()

x = df[ 'Ciśnienie']
x = np.array(x).reshape(-1,1)

y = df["Temperatura"]
y = np.array(y).reshape(-1,1)

reg = LinearRegression().fit(x,y)
x_new = x
y_new = reg.predict(x_new)

# plot regression line
# ax = sns.scatterplot(x='Ciśnienie', y="Temperatura", dane=df)

sns.relplot(x=df['Ciśnienie'], y=df["Temperatura"], data=df)
sns.lineplot(x = x_new[:,0],y = y_new[:,0], color='green')
# ax.set(xlabel='X', ylabel='Y')
plt.show()
# R Squared
print(f'R Squared: {reg.score(x,y)}')