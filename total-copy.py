from deepsurv import deep_surv
#from deepsurv.deepsurv_logger import DeepSurvLogger, TensorboardLogger
#from deepsurv import utils
from deepsurv import viz

import lasagne
import xlrd
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import pylab

from lifelines import KaplanMeierFitter
from lifelines.statistics import logrank_test

from datetime import datetime

def train_test_split(data,train_size = 0.8):
    length = list(data.shape)[0]
    if len(list(data.shape)) == 2:
        train_data = data[0:int(length*train_size),:]
        test_data = data[int(length*train_size):,:]
    else:
        train_data = data[0:int(length*train_size)]
        test_data = data[int(length*train_size):]
    return (train_data,test_data)

def plot_metrics(n_epochs,metrics,title_name,file_name):
    epochs = [epoch for epoch in range(n_epochs)]
    epochs2 = [epoch for epoch in range(len(metrics['valid_ci']))]
    plt.plot(epochs,metrics['train_ci'])
    plt.plot(epochs2,metrics['valid_ci'])
    plt.title(title_name)
    plt.xlabel('Epoch')
    plt.ylabel('Training Concordance Index')
    plt.savefig(file_name,dpi = 300)
    plt.show()

path = 'totalData.xlsx'
data = xlrd.open_workbook(path)
table = data.sheets()[0]

# data = pd.read_excel(path)
# table = data[data['roadnumber']==3]


e = np.array(table.col_values(1)[1:],dtype = np.int32)
n = len(e)
# len(e)
d = 10

x = np.zeros((n,d),dtype = np.float32)
for i in range(d):
    x[:,i] = list(np.array(table.col_values(5+i)[1:]))

t = np.zeros((n,4),dtype = np.float32)
for i in range(4):
    t[:,i] = list(np.array(table.col_values(2+i)[1:]))

(x_train,x_test) = train_test_split(x)
(t_train,t_test) = train_test_split(t)
(e_train,e_test) = train_test_split(e)

train_data = list()
for i in range(4):
    train_data.append({'x':x_train,'t':t_train[:,i],'e':e_train})

test_data = list()
for i in range(4):
    test_data.append({'x':x_test,'t':t_test[:,i],'e':e_test})

hyperparams = {
    'L2_reg': 15.0,
    'batch_norm': True,
    'dropout': 0.4,
    'hidden_layers_sizes': [25, 25],
    'learning_rate': 1e-05,
    'lr_decay': 0.001,
    'momentum': 0.9,
    'n_in': train_data[0]['x'].shape[1],
    'standardize': True
}

model = deep_surv.DeepSurv(**hyperparams)
try:
    model.load_weights('total_weight.h5')
except:
    pass
finally:
    pass
logger = None
update_fn=lasagne.updates.nesterov_momentum
n_epochs = 2000
valid_freq = n_epochs

time_names = ['Preparation Time','Travel Time','Clear Time','Total Time']
weights_file_names = ['Weights for '+x for x in time_names]
title_names = ['Training Concordance Index For ' +x for x in time_names]
time_name = time_names[3]
weights_file_name = weights_file_names[3]
title_name = title_names[3]

start = datetime.now()
metrics = model.train(train_data[3],test_data[3],n_epochs,
                      validation_frequency=valid_freq,
                       update_fn=update_fn)
end = datetime.now()
print('Total Training Time: '+str(end-start))

result = float(model.get_concordance_index(**test_data[3]))
model.save_weights('total_weight.h5')
print(result)
with open('result.txt','a') as f:
	f.write(str(n_epochs)+" " + str(result))
	f.write('\n')
# plot_metrics(n_epochs,metrics,title_name,time_name)
