"""Downloads all of the required datasets to run the program"""
import requests

# Gets transport_data_mod.csv
csv_url = 'https://raw.githubusercontent.com/jacobdesousa/csc110_project/main/transport_data_mod.csv'

req = requests.get(csv_url)
url_content = req.content
csv_file = open('transport_data_mod.csv', 'wb')

csv_file.write(url_content)
csv_file.close()

# Gets covid_cases_mod.csv
csv_url = 'https://raw.githubusercontent.com/jacobdesousa/csc110_project/main/covid_cases_mod.csv'

req = requests.get(csv_url)
url_content = req.content
csv_file = open('covid_cases_mod.csv', 'wb')

csv_file.write(url_content)
csv_file.close()
