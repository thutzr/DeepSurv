import pandas as pd

path = './processedData.csv'
excel_path = './processedData.xlsx'

pd.read_csv(path).to_excel(excel_path)

