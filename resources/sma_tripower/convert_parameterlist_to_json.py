from bs4 import BeautifulSoup
import json

# Step 1: Read the HTML file
with open('/workspaces/heim/data/sma_tripower/parameterlist_de.html', 'r') as file:
    html_content = file.read()

# Step 2: Parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Step 3: Find the table and extract data
table = soup.find('table')  # Adjust this if there are multiple tables or use a more specific identifier
rows = table.find_all('tr')

data = []
for row in rows:
    cols = row.find_all(['th', 'td'])
    cols = [ele.text.strip() for ele in cols]
    data.append(cols)

# Assuming the first row is the header
header = data[0]
json_data = [dict(zip(header, row)) for row in data[1:]]

# in json_data convert all unicode strings that are German Umlauts to ASCII
for row in json_data:
    for key, value in row.items():
        if isinstance(value, str):
            row[key] = value.replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue').replace('ß', 'ss')

# Convert all \u2012 to -
for row in json_data:
    for key, value in row.items():
        if isinstance(value, str):
            row[key] = value.replace('\u2012', '-')

# Convert all \u00a0 to a space
for row in json_data:
    for key, value in row.items():
        if isinstance(value, str):
            row[key] = value.replace('\u00a0', ' ')

# Convert all zusammenh\u00e4ngender to the string zusammenhaengender
for row in json_data:
    for key, value in row.items():
        if isinstance(value, str):
            row[key] = value.replace('zusammenh\u00e4ngender', 'zusammenhaengender')

# remove all entries in json_data, where the parameter "Gruppe" doesn't contain "Battery" as a substring
json_battery = []
for row in json_data:
    if "Batterie" in row["Gruppe"]:
        json_battery.append(row)

# remove all entries in json_data, where the parameter "Gruppe" doesn't contain "Wechselrichter" as a substring
json_wechselrichter = []
for row in json_data:
    if "Wechselrichter" in row["Gruppe"]:
        json_wechselrichter.append(row)
with open('wechselrichter.json', 'w') as json_file:
    json.dump(json_wechselrichter, json_file, indent=4)




# Step 4: Write the JSON data to a file
with open('modbus_params_sma_tripower.json', 'w') as json_file:
    json.dump(json_data, json_file, indent=4)

