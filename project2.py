"""
CSC110: Project Part 2
Jacob DeSousa, Marco Marchesano, Siddharth Arya
Analysis of COVID-19 case data in relation to transportation trends in the UK.
"""
from dataclasses import dataclass
import datetime
import csv
import dash
import pandas


@dataclass
class CaseData:
    """
    Formatted data from the COVID-19 case data

    Representation Invariants:
      - self.new_cases >= 0
      - self.cum_cases >= 0
    """
    date: datetime.date
    new_cases: int
    cum_cases: int


@dataclass
class TransportationData:
    """
    Formatted data from the UK transport dataset. -1 integer value represents no data for that given entry.

    Representation Invariants:
      - self.cars >= -1
      - self.light_commercial_vehicles >= -1
      - self.heavy_goods_vehicles >= -1
      - self.all_motor_vehicles >= -1
      - self.national_rail >= -1
      - self.london_tube >= -1
      - self.london_buses >= -1
      - self.national_buses >= -1
      - self.cycling >= -1
    """
    date: datetime.date
    cars: int
    light_commercial_vehicles: int
    heavy_goods_vehicles: int
    all_motor_vehicles: int
    national_rail: int
    london_tube: int
    london_buses: int
    national_buses: int
    cycling: int


def load_case_data(path: str) -> list[CaseData]:
    """ Return a list of case data from csv file. """
    data = []

    with open(path) as file:
        reader = csv.reader(file, delimiter=',')
        next(reader)

        for row in reader:
            assert len(row) == 6
            date = datetime.date(int(row[3][0:4]), int(row[3][5:7]), int(row[3][8:10]))
            new_cases = int(row[4])
            cum_cases = int(row[5])
            data.append(CaseData(date, new_cases, cum_cases))

    return data


def load_transport_data(path: str) -> list[TransportationData]:
    """ Return a list of transportation data from csv file. """
    data = []

    with open(path) as file:
        reader = csv.reader(file, delimiter=',')
        next(reader)
        for row in reader:
            assert len(row) == 10
            for i in range(10):
                if row[i] == '..':
                    row[i] = '-1'
            date = datetime.date(int(row[0][6:10]), int(row[0][3:5]), int(row[0][0:2]))
            cars = int(row[1].removesuffix('%'))
            lcv = int(row[2].removesuffix('%'))
            hgv = int(row[3].removesuffix('%'))
            mv = int(row[4].removesuffix('%'))
            nr = int(row[5].removesuffix('%'))
            lt = int(row[6].removesuffix('%'))
            lb = int(row[7].removesuffix('%'))
            nb = int(row[8].removesuffix('%'))
            cyc = int(row[9].removesuffix('%'))
            data.append(TransportationData(date, cars, lcv, hgv, mv, nr, lt, lb, nb, cyc))

    return data


graph_data = 'Testing'
print(graph_data)
