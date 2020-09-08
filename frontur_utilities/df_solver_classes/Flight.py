from dataclasses import dataclass, field
from pandas import DataFrame, Timedelta
from math import floor, ceil
import frontur_utilities.constants as const

@dataclass(unsafe_hash=True)
class Flight:
    flight_entry: DataFrame = field(repr=False, hash=False)
    seats_used: float = field(default=.8, repr=False, metadata={'unit': 'normalized percentage'})
    poll_success: float = field(default=.6, repr=False, metadata={'unit': 'normalized percentage'})
    poll_time: int = field(default=Timedelta(seconds=30).seconds, repr=False, metadata={'unit': 'seconds'})
    seats: int = field(init=False)
    flight_day: Timedelta = field(init=False)
    flight_hour: int = field(init=False)
    index: int = field(init=False)
    surveys: int = field(init=False)
    time_consumed: int = field(init=False, repr=False, metadata={'unit': 'seconds'})

    def __post_init__(self):
        self.index = int(self.flight_entry.index[0])
        self.seats = int(self.flight_entry.iloc[0][const.DF_SEATS])
        self.flight_day = self.flight_entry.iloc[0][const.DF_DAY_COL_NAME]
        self.flight_hour = self.flight_entry.iloc[0][const.DF_EMBARK_HOUR].seconds
        self.surveys = ceil(ceil(self.seats * self.seats_used) * self.poll_success)
        self.time_consumed = self.surveys * self.poll_time
        
    def __str__(self):
        return f'{self.index} Day {self.flight_day + self.flight_hour} · {self.seats} seats - {self.surveys} Aproximated viable interviews'