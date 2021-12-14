"""
CSC110: Project Part 2
Jacob DeSousa, Marco Marchesano, Siddharth Arya

The get_files module downloads the required datasets for use by the rest of the program.
"""

import os
import requests
import python_ta


def download_datasets() -> None:
    """
    Downloads the required datasets from GitHub if they do not already exist.

    :return: No return. Downloads files into current directory.
    """
    # Gets transport_data_mod.csv
    if not os.path.isfile('transport_data_mod.csv'):
        csv_url = 'https://raw.githubusercontent.com/jacobdesousa/' \
                  'csc110_project/main/transport_data_mod.csv'

        req = requests.get(csv_url)
        url_content = req.content
        with open('transport_data_mod.csv', 'wb') as csv_file:
            csv_file.write(url_content)

    # Gets covid_cases_mod.csv
    if not os.path.isfile('covid_cases_mod.csv'):
        csv_url = 'https://raw.githubusercontent.com/jacobdesousa' \
                  '/csc110_project/main/covid_cases_mod.csv'

        req = requests.get(csv_url)
        url_content = req.content
        with open('covid_cases.csv', 'wb') as csv_file:
            csv_file.write(url_content)


if __name__ == '__main__':
    python_ta.check_all(config={
        'extra-imports': ['python_ta', 'os', 'requests'],
        'allowed-io': ['download_datasets'],
        'max-line-length': 100,
        'disable': ['R1705', 'C0200']
    })
