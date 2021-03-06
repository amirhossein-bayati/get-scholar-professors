import json

import pandas as pd
import sys

"""This module reads all data that 
scraped from google scholar ('Json/final.json' file)
and convert them to the excel file.
"""

with open(sys.argv[1], "r") as f:
    # Reading from file
    data = json.loads(f.read())
    # Convert it to Dataframe
    df = pd.json_normalize(data)

# Export Dataframe to an Excel file
file_name = "Final_Dataset.xlsx"
df.to_excel(file_name, index=False)
