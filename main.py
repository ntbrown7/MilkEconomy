import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

headers = {'Content-type': 'application/json'}
data = json.dumps({"seriesid": ['APU0000709112'],"startyear":"1995", "endyear":"2023"})

response = requests.post('https://api.bls.gov/publicAPI/v2/timeseries/data/', data=data, headers=headers)

json_data = json.loads(response.text)

data_list = []
for series in json_data['Results']['series']:
    seriesId = series['seriesID']
    for item in series['data']:
        year = item['year']
        # BLS API uses 'M01' for January, 'M02' for February, etc.
        month = int(item['period'][1:])  # Strip the 'M' and convert to an integer
        value = item['value']
        data_list.append([year, month, value])

# Convert to a DataFrame
df = pd.DataFrame(data_list, columns=['Year', 'Month', 'Value'])
df['Value'] = pd.to_numeric(df['Value'])

# Create a datetime column from the year and month
df['Date'] = pd.to_datetime(df[['Year', 'Month']].assign(day=1))
df = df.sort_values('Date')

# Plot data
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(df['Date'], df['Value'])
ax.set_xlabel('Time')
ax.set_ylabel('Price of Milk')
ax.set_title('Price of Milk Over Time')

# Format the x-axis to show the YEAR-MONTH
date_form = DateFormatter("%Y-%m")
ax.xaxis.set_major_formatter(date_form)

plt.show()
