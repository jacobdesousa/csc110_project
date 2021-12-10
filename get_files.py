"""Downloads all of the required datasets to run the program"""

import requests

# Gets transport_data.csv
csv_url = 'https://raw.githubusercontent.com/jacobdesousa/csc110_project/main/transport_data.csv?token=APIG3PZY3WVZ6WLEPCOE3ZLBWOXVQ'

req = requests.get(csv_url)
url_content = req.content
csv_file = open('transport_data.csv', 'wb')

csv_file.write(url_content)
csv_file.close()

# Gets covid_cases.csv
csv_url = 'https://raw.githubusercontent.com/jacobdesousa/csc110_project/main/covid_cases.csv?token=APIG3P3SRJGU5B4BNTG2WG3BWOXJU'

req = requests.get(csv_url)
url_content = req.content
csv_file = open('covid_cases.csv', 'wb')

csv_file.write(url_content)
csv_file.close()

# Gets covid_cases_mod.csv
csv_url = 'https://raw.githubusercontent.com/jacobdesousa/csc110_project/main/covid_cases_mod.csv?token=APIG3P2IJ5OGSYHV2K5IVTLBWOXMK'

req = requests.get(csv_url)
url_content = req.content
csv_file = open('covid_cases_mod.csv.csv', 'wb')

csv_file.write(url_content)
csv_file.close()

