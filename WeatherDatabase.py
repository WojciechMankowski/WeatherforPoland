from sqlalchemy import create_engine, String, Integer, Column, DateTime, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()
HOST="46.41.140.135"
USER="wojtek"
PASSWORD="Wojtek92!"
DATABASE_NAME='Flask'

class WeatherData(Base):
    __tablename__ = 'WeatherData'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=func.now())
    city = Column(String(length=100))
    temperature = Column(String(100))
    humidity = Column(String(100))
    Precipitation = Column(String(100))
    pressure = Column(String(100))

    def __init__(self, data):
        self.date = data['date']
        self.temperature = data['temp']
        self.humidity = data['humidity']
        self.pressure = data['pressure']
        self.city = data['city']
        self.Precipitation = data["pressure"]

    def __str__(self):
        return "date='%s', temperature='%s', humidity='%s', pressure='%s', city='%s')" % (
            self.date, self.temperature, self.humidity, self.pressure, self.city)

if __name__ == '__main__':
    text_connect = f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}/{DATABASE_NAME}"
    engine = create_engine(text_connect)
    Base.metadata.create_all(engine)
