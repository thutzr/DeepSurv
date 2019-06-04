import pandas as pd
import matplotlib.pyplot as plt
from lifelines import KaplanMeierFitter
import lifelines
path = './totalData.xlsx'

data = pd.read_excel(path)
duration = data.totaltime
indicator = data.failure
kmf = KaplanMeierFitter()

kmf.fit(duration,indicator)
ax = lifelines.plotting.plot_lifetimes(durations = duration,event_observed = indicator)
ax.grid(axis = 'x')

kmf.plot()

plt.title('Survival Function')
plt.show()
