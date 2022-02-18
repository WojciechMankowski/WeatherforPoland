from pydantic import BaseModel
import datetime

class DataPydantic(BaseModel):
    Date: datetime.datetime
    City: str = None
    Temp: str = None
    Humidity: str = None
    Precipitation: str = None
    Pressure: str = None

    def PrepareTheData(self):
        return {"date": self.Date,"city": self.City,"temp": self.Temp,  "humidity": self.Humidity,"precipitation": self.Precipitation,
                "pressure": self.Pressure}
