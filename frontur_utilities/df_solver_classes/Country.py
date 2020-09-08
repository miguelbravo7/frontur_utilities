from dataclasses import dataclass, field
from typing import List, Dict
from pandas import DataFrame, Timedelta
from frontur_utilities.df_solver_classes import Flight, parameter_initializers as pinit
from frontur_utilities import utility_df

@dataclass()
class Country:
    dataframe: DataFrame = field(repr=False)
    index: int = field(repr=False)
    country_name: str
    num_travelers: int    
    interviews: dict = field(metadata={'description': 'Map of minimum interviews'})
    ine_polls: int = field(default=0)
    min_polls: int = field(init=False)
    flights: List[Flight.Flight] = field(init=False, default_factory=list, metadata={'description': 'List of Flight dataobjects'})
    flight_numbers: Dict[int, int] = field(init=False, repr=False, default_factory=dict, metadata={'description': 'Dictionary of Flight dataobject indexes'}) 

    plane_kwargs: Dict = field(default_factory=dict, repr=False)

    def __post_init__(self):
        self.min_polls = utility_df.minimum_sample(self.num_travelers, self.interviews)
        for i in range(len(self.dataframe.index)):
            self.flights.append(Flight.Flight(self.dataframe.iloc[[i]], **self.plane_kwargs))
            self.flight_numbers[self.dataframe.index[i]] = i

    def assigned_flights(self, selected_entrys):
        good_keys = self.dataframe.index.intersection(selected_entrys)
        acc = 0
        for i in set(good_keys) & set(self.flight_numbers.keys()):
            acc += self.flights[self.flight_numbers[i]].surveys
        msg = f'{len(good_keys)} flights · {acc} surveys'
        if len(good_keys):
            msg += '\n' + self.dataframe.loc[good_keys].to_string(header=False)
        return msg

    def __str__(self):
        msg = f'Country: {self.country_name}'
        msg += f'\nTravelers: {self.num_travelers}'
        msg += f'\nMinimum required polls: {self.min_polls}'
        msg += f'\nINE polls done: {self.ine_polls}'
        msg += f'\nFlights: {len(self.flights)}'
        # for flight in self.flights:
        #     msg += '\n' + flight.__str__()
        return msg