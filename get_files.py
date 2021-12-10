"""Downloads all of the required datasets to run the program"""

# DO NOT RUN THIS FILE IT WILL OVERWRITE THE CSV FILES WITH NOTHING
# WE HAVE TO GET THE URL FOR THE CSV FILES

import requests

# Gets transport_data.csv
csv_url = ''

req = requests.get(csv_url)
url_content = req.content
csv_file = open('transport_data.csv', 'wb')

csv_file.write(url_content)
csv_file.close()

# Gets covid_cases.csv
csv_url = ''

req = requests.get(csv_url)
url_content = req.content
csv_file = open('covid_cases.csv', 'wb')

csv_file.write(url_content)
csv_file.close()

# Gets covid_cases_mod.csv
csv_url = ''

req = requests.get(csv_url)
url_content = req.content
csv_file = open('covid_cases_mod.csv.csv', 'wb')

csv_file.write(url_content)
csv_file.close()
