from dataclasses import dataclass, field
from typing import List, Dict
from pandas import DataFrame, Timedelta
from frontur_utilities.df_solver_classes import Country, parameter_initializers as pinit

@dataclass(frozen=True)
class SolverParameters:
    dataframe: DataFrame = field(repr=False)
    pollsters: List = field(default_factory=pinit.initialize_pollsters)
    countries: List[Country.Country] = field(init=False, default_factory=list, metadata={'description': 'List of Country dataobjects'})

    workday_time: int = field(default=Timedelta(hours=8).seconds, metadata={'unit': 'hours'})
    rest_time: int = field(default=Timedelta(minutes=10).seconds, metadata={'unit': 'minutes'})
    execution_time_limit: int = field(default=Timedelta(minutes=15).seconds, metadata={'unit': 'minutes'})

    country_kwargs: Dict = field(default_factory=dict, repr=False)

    def __post_init__(self):
        index=0
        for country_name, row in self.dataframe.groupby(['Pais']).sum().iterrows():
            if country_name != 'ESPAÑA':
                self.countries.append(Country.Country(
                    self.dataframe.loc[lambda frame: frame['Pais'] == country_name],
                    index,
                    country_name,
                    int(row['asientos']),
                    **self.country_kwargs
                ))
                index+=1
            else:
                for city_name, row in self.dataframe.loc[lambda frame: frame['Pais'] == 'ESPAÑA'].groupby(['Destino']).sum().iterrows():
                    self.countries.append(Country.Country(
                        self.dataframe.loc[lambda frame: frame['Destino'] == city_name],
                        index,
                        city_name,
                        int(row['asientos']),
                        **self.country_kwargs
                    ))
                    index+=1
    
    @property
    def flights(self) -> list:
        for country in self.countries:
            for flight in country.flights:
                yield flight

    @property
    def num_flights(self) -> int:
        acc = 0
        for country in self.countries:
            acc += len(country.flights)
        return acc
    
    @property
    def num_pollsters(self) -> int:
        return len(self.pollsters)

    @property
    def num_countries(self) -> int:
        return len(self.countries)
        
    def __str__(self):
        msg = f'Execution time limit: {self.execution_time_limit}\n'
        msg += f'Pollsters: {self.pollsters}\n'
        msg += f'Countries: {len(self.countries)}\n'
        for country in self.countries:
            msg += country.__str__() + '\n'
        return msg
