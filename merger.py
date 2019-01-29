import csv
import pandas as pd

tagname = input('input tag name: ' )


df1 = pd.read_csv(tagname + '_OrganizationsList_with_IDs.csv')
df2 = pd.read_csv(tagname + '_ContactEmailList.csv')

with open(tagname + '_Filtered.csv', 'w') as output:
    pd.merge(df1, df2, on='Hospital ID').to_csv(output, index=False)

print('======Merger.py complete======')
print('Make sure to check for and remove any duplicate records')
