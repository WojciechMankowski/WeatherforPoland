from typing import Union
from API import APIConnection
from SaveInFille import SaveInDatabase
import datetime


def run_example():
    URL: str = "https://danepubliczne.imgw.pl/api/data/synop"
    api: APIConnection = APIConnection(URL)
    dane: list[dict[str, str]] = api.Connection()
    api.SelectionOfItems(dane)
    dic: list[Union[list[str], list[datetime.datetime]]] = api.CreateADictionaryForWriting()

    data = datetime.datetime.now().date()
    data = str(data.strftime('%Y_%m_%d'))
    databese = SaveInDatabase()
    checks = databese.CheckFile(data)
    lastdate = str(api.Date[-1])
    lastData = False
    if checks != False:
        lastData = databese.CheckData(data, lastdate)
        databese.save(data, dic)
    if lastData == False:
        databese.save(data,dic)
if __name__ == '__main__':
    run_example()