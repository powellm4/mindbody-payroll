import numbers
import pandas as pandas
from StudentEntry import StudentEntry

print("\n------------------------------\n\nBeginning MindBody Payroll\n\n------------------------------\n\n\n")
h = StudentEntry()
print(h.r)
print('\n\n')
df = pandas.read_csv('/Users/marshallpowell/Desktop/For Marshall - Sheet1.csv')
print(df.head())
