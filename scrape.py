import requests
from bs4 import BeautifulSoup
import pandas as pd
from pathlib import Path
import numpy as np

url_template = 'https://results.ridelondon.co.uk/2022/?page={page}&event=I&event_main_group=C&num_results=100&pid=list'
n_pages = 206

full_names = []
rider_numbers = []
finish_times = []

for i in range(n_pages):
    url = url_template.format(page=i)
    print(url)
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'html.parser')
    for row in soup.select('li.row'):
      cols = row.select('div.row')

      cell = cols[0].select('.type-fullname a')
      if len(cell) == 0:
        continue
      full_name = row.select('.type-fullname a')[0].text
      full_names.append(full_name)
      
      cell = cols[1].select('.list-field')
      if len(cell) == 0:
        continue
      rider_number = cell[0].text.replace('Rider Number', '')
      rider_numbers.append(rider_number)

      cell = cols[2].select('.list-field')
      if len(cell) == 0:
        continue
      finish_time = cell[0].text.replace('Finish', '')
      finish_times.append(finish_time)

df = pd.DataFrame({
  'position': np.arange(1, len(full_names)+1),
  'full_name': full_names, 
  'rider_number': rider_numbers, 
  'finish_time': finish_times})
df.sort_values(by=['finish_time'], inplace=True)
df['position'] = np.arange(1, len(df)+1)

filepath = Path('2022 Ride London 100.csv')
df.to_csv(filepath, index=False)
