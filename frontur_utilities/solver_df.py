from ortools.linear_solver import pywraplp
from frontur_utilities.df_solver_classes import SolverParameters
import json
import pandas
import frontur_utilities as df
import frontur_utilities.constants as const
import frontur_utilities.utility_functions as uf


def df_solver(data_frame, parameters={}, no_groups=False):
    data_frame[const.DF_EMBARK_HOUR] = pandas.to_timedelta(data_frame[const.DF_EMBARK_HOUR])
    data_frame[const.DF_DAY_COL_NAME] = pandas.to_datetime(data_frame[const.DF_DAY_COL_NAME], format="%d/%m/%Y")
    
    sol_par = SolverParameters.SolverParameters(data_frame, **parameters)
    solver = pywraplp.Solver('FronturSolver', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
    solver.SetTimeLimit(int(sol_par.execution_time_limit) * 1000)
    pollsters = range(sol_par.num_pollsters)

    x = { (i,k) : solver.BoolVar('x[%i, %i]' % (i, k)) for i in range(sol_par.num_flights) for k in pollsters }
    y1 = { (i) : solver.BoolVar('y1[%i]' % (i)) for i in range(sol_par.num_flights) }
    y2 = { (i) : solver.BoolVar('y2[%i]' % (i)) for i in range(sol_par.num_flights) }
    z = { (p) : solver.BoolVar('z[%i]' % (p)) for p in range(sol_par.num_countries) }

    [solver.Add(y1[i.index] + y2[i.index] <= 1) for i in sol_par.flights]
    [solver.Add(sum(x[i.index, k] for k in pollsters) == y1[i.index] + 2*y2[i.index]) for i in sol_par.flights]

    [solver.Add(sum(i.surveys * (y1[i.index] + y2[i.index]) for i in p.flights) >= (p.min_polls - p.ine_polls) * z[p.index]) for p in sol_par.countries]

    flights = list(sol_par.flights)
    for first in range(len(flights)):
        for second in range(first+1, len(flights)):
            i = flights[first]
            j = flights[second]
            if (i.flight_day == j.flight_day):
                if (i.flight_hour > j.flight_hour):
                    tmp = i
                    i = j
                    j = tmp
                if no_groups:
                    if (i.flight_hour > j.flight_hour - j.time_consumed/2 - sol_par.rest_time) or (i.flight_hour - i.time_consumed/2 < j.flight_hour - sol_par.workday_time): # - sol_par.rest_time
                        [ solver.Add( x[i.index, k] + x[j.index, k] <= 1 ) for k in pollsters]
                else:
                    if (i.flight_hour > j.flight_hour - j.time_consumed/2 - sol_par.rest_time) or (i.flight_hour - i.time_consumed/2 < j.flight_hour - sol_par.workday_time): # - sol_par.rest_time
                        [ solver.Add( x[i.index, k] + x[j.index, k] <= 1 ) for k in pollsters]
                    elif i.flight_hour > j.flight_hour - j.time_consumed - sol_par.rest_time:
                        [ solver.Add( x[i.index, k] + x[j.index, k] <= 1 + sum(x[i.index, k_not] for k_not in pollsters if k_not != k)) for k in pollsters ]
                    elif i.flight_hour - i.time_consumed < j.flight_hour + sol_par.workday_time:
                        [ solver.Add( x[i.index, k] + x[j.index, k] <= 1 + sum(x[j.index, k_not] for k_not in pollsters if k_not != k)) for k in pollsters ]

    solver.Maximize(sum(f.surveys*(y1[f.index] + y2[f.index]*2) for f in sol_par.flights) - 100*sum(p.num_travelers*(1-z[p.index]) for p in sol_par.countries))

    print('Number of variables =', solver.NumVariables())
    print('Number of constraints =', solver.NumConstraints())

    sol = solver.Solve()

    if(sol == solver.OPTIMAL):
        selected_entries = set([i for i in range(sol_par.num_flights) for k in pollsters if x[i, k].solution_value()])
        pollsters_assigns = [set([i for i in range(sol_par.num_flights) if x[i, k].solution_value()]) for k in pollsters]
        individual = set([i for i in range(sol_par.num_flights) if y1[i].solution_value()])
        dual = set([i for i in range(sol_par.num_flights) if y2[i].solution_value()])
        for k in pollsters:
            data_frame['Encuestador ' + str(k)] = ''
            data_frame.at[pollsters_assigns[k], 'Encuestador ' + str(k)] = 'X'
        print('Vuelos seleccionados')
        print(data_frame.loc[selected_entries][[
            const.DF_DAY_COL_NAME, const.DF_EMBARK_HOUR, const.DF_SEATS, *['Encuestador ' + str(k) for k in pollsters]
            ]].sort_values([const.DF_DAY_COL_NAME, const.DF_EMBARK_HOUR], ascending=[True, True]).to_string())
    else:
        print('Optimal solution not found on time')

    print("Time = ", solver.WallTime()/1000, " seconds")
    return data_frame
