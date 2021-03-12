import json
import numpy as np
import pandas as pd
import pickle5 as pickle


with open('Forbes.pkl', 'rb') as f:
    data = pickle.load(f)
    
df = data.loc[data["forbes_year"]=='2019']

#Try nearest neighbour based on PCA coordinates
df1 = df[['Company','PCA_1','PCA_2','PCA_3','pca_cluster','Sector','Revenue']].reset_index()

#Dataframe Preprocessing
data_2019 = df1.to_numpy()
for d in data_2019:
    d[0]-=22002
    
company_to_idx = {}
companyidx_to_sector = {}
idx_to_company = {}
companyidx_to_revenue = {}

for d in data_2019:
    company_to_idx[d[1].lower()] = d[0]
    idx_to_company[d[0]] = d[1]
    companyidx_to_sector[d[0]] = d[-2]
    companyidx_to_revenue[d[0]] = d[-1]
    
#Calculate pairwise distnace
company_distance = [[-1 for _ in range(len(data_2019))] for _ in range(len(data_2019))]

for i in range(len(data_2019)):
    for j in range(len(data_2019)):
        if data_2019[i][5]==data_2019[j][5]:
            dist = (data_2019[i][2] - data_2019[j][2])**2 + (data_2019[i][3] - data_2019[j][3])**2 + (data_2019[i][4] - data_2019[j][4])**2
            rev1,rev2 = data_2019[i][-1],data_2019[j][-1]
            
            rev_close = rev1/rev2 if rev1>=rev2 else rev2/rev1
            company_distance[i][j] = (dist+0.01*rev_close,j,data_2019[j][6],data_2019[j][7])
            
        else:
            company_distance[i][j] = (float('inf'),j)
            
        
    company_distance[i].sort(key = lambda x:x[0])
    
    
def k_closest(company,k):
    '''
    This function calculates k nearest companies to the company in query based on the metric calculated for distance
    input param: string, int
    ouput param: list[string]
    '''
    lst = company_distance[company_to_idx[company.lower()]]
    output = []
    for l in lst[1:k+1]:
        output.append((idx_to_company[l[1]],l[2],l[3]))
    
    return output