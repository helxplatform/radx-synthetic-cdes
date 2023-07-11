import pandas as pd
import yaml 

df = pd.read_csv('/Users/asiyahahmad/Documents/GitHub/radx-synthetic-cdes/drugs data - data.csv')

df['Normal_Pct'] = df['Cumulative Percentage'].diff().fillna(df['Cumulative Percentage'])

list = []
dictionary = df.to_dict(orient='records')
for row in dictionary:
    list.append({
        'response_name': row['Drug To Use'],
        'response_value': row['Drug To Use'],
        'frequency': row['Normal_Pct']
    })
with open('drugstempfile.yaml', 'w+') as file:
    yaml.dump(list, file)


