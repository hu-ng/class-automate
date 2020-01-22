import pandas as pd
from datetime import date, time

# Date in isoformat: YYYY-MM-DD
# Time in isoformat: HH:MM:SS
# NO SPACES

data = pd.read_csv('test.csv')

class StudentData:
    def __init__(self, row_data):
        self.name = row_data["Student Name"]
        self.day = date.fromisoformat(row_data["Day"]).strftime("%m/%d/%Y")
        self.time = time.fromisoformat(row_data["Time"].split(" ")[0])
        self.am_pm = row_data["Time"].split(" ")[1].lower()
        self.email = row_data["Student Email"]