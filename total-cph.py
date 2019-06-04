from lifelines import CoxPHFitter
import numpy as np
import pandas as pd
import lifelines

path = './totalData.xlsx'

data = pd.read_excel(path)
col = list(data.columns)
del col[0:5]

cph = CoxPHFitter()
cph.fit(data,'totaltime','failure',strata=col)

cph.print_summary()
cph.predict_cumulative_hazard(data)
