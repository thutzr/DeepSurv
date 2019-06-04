import pandas as pd

path = './Data.xlsx'
rawData = pd.read_excel(path,sheet_name = 'totaltime')

rawData['season'] = 4 - rawData['spring']*3 - rawData['summer']*2-rawData['autumn']*3
del rawData['spring']
del rawData['summer']
del rawData['autumn']

rawData['treat'] = 4 - rawData['treat1']*3 - rawData['treat2']*2-rawData['treat3']*3
del rawData['treat1']
del rawData['treat2']
del rawData['treat3']

rawData['accident type'] = 6 - rawData['rear']*5 - rawData['crash']*4 - rawData['nonmotor']*3 - rawData['stable']*2 - rawData['turnover']*1
del rawData['rear']
del rawData['crash']
del rawData['nonmotor']
del rawData['stable']
del rawData['turnover']

rawData['vehicle'] = 4 - rawData['taxi']*3 - rawData['bus']*2 - rawData['truck']*1
del rawData['taxi']
del rawData['bus']
del rawData['truck']

failure = rawData['failure']
rawData.drop(labels = ['failure'],axis = 1,inplace=True)
rawData.insert(0,'failure',failure)

savePath = r'./processedData.xlsx'
rawData.to_excel(savePath,index=False)
