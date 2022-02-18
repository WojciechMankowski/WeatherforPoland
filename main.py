from zoneinfo import ZoneInfo
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from API import APIConnection
import datetime
from WeatherDatabase import WeatherData

HOST="46.41.140.135"
USER="wojtek"
PASSWORD="Wojtek92!"
DATABASE_NAME='Flask'

def Convert_str_to_datetime(data_in_api_str):
    format_datatime = "%Y-%m-%d %H:%M:00"
    date_string = data_in_api_str[:19]
    date_object =  datetime.datetime.strptime(date_string, format_datatime)
    return date_object

def SaveInDataBase(data, date):
    text_connect = f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}/{DATABASE_NAME}"
    print(text_connect)
    engine = create_engine(text_connect)
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    data_in_the_database = session.query(WeatherData).all()[-1].date
    print(data_in_the_database != date)
    if data_in_the_database != date:
        for item in data:
            newdata = WeatherData(item.PrepareTheData())
            session.add(newdata)
    session.commit()
    session.close()


def run_example():
    URL: str = "https://danepubliczne.imgw.pl/api/data/synop"
    api: APIConnection = APIConnection(URL)
    dane: list[dict[str, str]] = api.Connection()
    api.SelectionOfItems(dane)
    data = api.getDataSet()
    data_in_api = Convert_str_to_datetime(f"{data[0].Date}")
    SaveInDataBase(data, data_in_api)

if __name__ == '__main__':
    run_example()
