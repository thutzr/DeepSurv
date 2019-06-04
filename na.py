import numpy as np
import pandas as pd

from lifelines import NelsonAalenFitter

path = './totalData.xlsx'
data = pd.read_excel(path)

duration = data.totaltime

indicator = data.failure

naf = NelsonAalenFitter()

naf.fit(duration,indicator)

naf.plot()
