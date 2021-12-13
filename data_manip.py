"""
CSC110: Project Part 2
Jacob DeSousa, Marco Marchesano, Siddharth Arya

Data Manipulation functions such as class definitions, loading data,
and manipulating data are in this module.
"""

import csv
import datetime
import math
from dataclasses import dataclass

import python_ta


@dataclass
class CaseData:
    """
    Formatted data from the COVID-19 case data

    Instance Attributes
      - date: the date of which the data was collected
      - num_cases: the number of cases recorded at the given date
      - cum_cases: the number of cumulative cases in the UK

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
    Formatted data from the UK transport dataset. -1 integer value
    represents no data for that given entry.

    Instance Attributes:
     -  date: the date of when the data was collected
     -  cars: the percentage of cars being used at the given date
     -  light_commercial_vehicles: the percentage of light commercial vehicles being used
     -  heavy_goods_vehicles: the percentage of heavy goods vehicles being used
     -  all_motor_vehicles: the general percentage of all motor vehicles being used
     -  national_rail: the percentage of which trains are used
     -  london_tube: the percentage the London tube was being used
     -  london_buses: the percentage of London buses being used
     -  cycling: the percentage of bicycles being used

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
    """
    Returns a list of CaseData read from the csv file at path.

    :param path: The path to the file to load data from.
    :return: A list of CaseData loaded from path.
    """
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
    """
    Returns a list of TransportationData read from the csv file at path.
    Entries missing from the data, represented as '..', will be stored as -1.

    :param path: The path to the file to load data from.
    :return: A list of TransportationData loaded from path.
    """
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


def average_case_data(data: list[CaseData], grouping: int) -> list[CaseData]:
    """
    Returns a list of CaseData.
    The entries in data are grouped by grouping number of elements which are averaged together.

    :param data: CaseData objects in a list
    :param grouping: How many entries in data to group together.
    :return: Resulting list of averaged CaseData.

    Preconditions:
        - 0 < grouping < 30
    """
    averaged_data = []

    count = len(data)
    while count > 0:
        count -= grouping
        grouped = data[0:min(grouping, len(data))]
        data = data[grouping:len(data)]
        date, new_cases, cum_cases = None, 0, 0
        for i in range(0, min(grouping, len(data))):
            new_cases += grouped[i].new_cases
            cum_cases += grouped[i].cum_cases
            if i == min(grouping, math.ceil(len(data) / 2)) - 1:
                date = grouped[i].date
        averaged_data.append(CaseData(date, round(new_cases / min(grouping, len(grouped))),
                                      round(cum_cases / min(grouping, len(grouped)))))

    return averaged_data


def average_transport_data(data: list[TransportationData], grouping: int) \
        -> list[TransportationData]:
    """
    Returns a list of TransportationData.
    The entries in data are grouped by grouping number of elements which are averaged together.

    :param data: TransportationData objects in a list
    :param grouping: How many entries in data to group together.
    :return: Resulting list of averaged TransportationData.

    Preconditions:
        - 0 < grouping < 30
    """
    averaged_data = []

    count = len(data)
    while count > 0:
        count -= grouping
        grouped = data[0:min(grouping, len(data))]
        data = data[grouping:len(data)]
        date = None
        cars, lcv, hgv, mv, nr, lt, lb, nb, cyc = 0, 0, 0, 0, 0, 0, 0, 0, 0
        for i in range(0, min(grouping, len(grouped))):
            cars += grouped[i].cars
            lcv += grouped[i].light_commercial_vehicles
            hgv += grouped[i].heavy_goods_vehicles
            mv += grouped[i].all_motor_vehicles
            nr += grouped[i].national_rail
            lt += grouped[i].london_tube
            lb += grouped[i].london_buses
            nb += grouped[i].national_buses
            cyc += grouped[i].cycling
            if i == min(grouping, math.ceil(len(grouped) / 2)) - 1:
                date = grouped[i].date
        averaged_data.append(TransportationData(date,
                                                round(cars / min(grouping, len(grouped))),
                                                round(lcv / min(grouping, len(grouped))),
                                                round(hgv / min(grouping, len(grouped))),
                                                round(mv / min(grouping, len(grouped))),
                                                round(nr / min(grouping, len(grouped))),
                                                round(lt / min(grouping, len(grouped))),
                                                round(lb / min(grouping, len(grouped))),
                                                round(nb / min(grouping, len(grouped))),
                                                round(cyc / min(grouping, len(grouped)))))

    return averaged_data


if __name__ == '__main__':
    python_ta.check_all(config={
        'extra-imports': ['dataclasses', 'datetime', 'csv', 'python_ta', 'math'],
        'allowed-io': ['load_case_data', 'load_transport_data'],
        'max-line-length': 100,
        'disable': ['R1705', 'C0200']
    })
