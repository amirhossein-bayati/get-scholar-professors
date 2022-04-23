import json

import pandas as pd

# JSON file
f = open ('final.json', "r")
 
# Reading from file
data = json.loads(f.read())
# Convert it to Dataframe
df = pd.json_normalize(data)

# Export Dataframe to an Excel file
file_name = 'Final_Dataset.xlsx'
df.to_excel(file_name,index=False)

