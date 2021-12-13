"""CSC110: Project Part 2
Jacob DeSousa, Marco Marchesano, Siddharth Arya
Analysis of COVID-19 case data in relation to transportation trends in the UK.
"""
import os
import requests
import python_ta


def download_datasets() -> None:
    """Downloads all of the required datasets to run the program"""
    # Gets transport_data_mod.csv
    if not os.path.isfile('transport_data_mod.csv'):
        csv_url = 'https://raw.githubusercontent.com/jacobdesousa/' \
                  'csc110_project/main/transport_data_mod.csv'

        req = requests.get(csv_url)
        url_content = req.content
        with open('transport_data_mod.csv', 'wb') as csv_file:
            csv_file.write(url_content)

    if not os.path.isfile('covid_cases_mod.csv'):
        # Gets covid_cases_mod.csv
        csv_url = 'https://raw.githubusercontent.com/jacobdesousa' \
                  '/csc110_project/main/covid_cases_mod.csv'

        req = requests.get(csv_url)
        url_content = req.content
        with open('transport_data_mod.csv', 'wb') as csv_file:
            csv_file.write(url_content)


if __name__ == '__main__':
    python_ta.check_all(config={
        'extra-imports': ['python_ta', 'os', 'requests'],
        'allowed-io': ['download_datasets'],
        'max-line-length': 100,
        'disable': ['R1705', 'C0200']
    })
