import csv
import pandas as pd

tagname = input('input tag name: ' )


df1 = pd.read_csv(tagname + '_OrganizationsList_with_Emails.csv')
df2 = pd.read_csv(tagname + '_ContactEmailList.csv')

with open(tagname + '_Filtered_with_Emails.csv', 'w', encoding="utf-8") as output:
    pd.merge(df1, df2, on='Hospital ID').to_csv(output, index=False)

print('Merger.py complete')
print('==== Make sure to check for and remove any duplicate records'=====)
print("==== Sepeate email column.  May contain more than one email in the column ====")
