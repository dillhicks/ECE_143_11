#Predictions
import numpy as np
import itertools
from sklearn.linear_model import LinearRegression
# RFE is an efficient approach for eliminating features 
# from a training dataset for feature selection
from sklearn.feature_selection import RFE
from sklearn.model_selection import cross_val_score

def perform_predictions(cols,years,df):
    #columns to use for predictions
    pred_cols = ['Company']
    # add column names with format like 'Market value 2017'
    temp = list(itertools.product(cols, years))
    pred_cols.extend([ "%s %s" % x for x in temp])
    # drop companies with stats containing 'nan'
    df_pred = df[pred_cols].dropna()

    # stats from 2017-2019
    X = df_pred.filter(regex='|'.join(str(x) for x in list(years[:-1])))
    # stats in 2020
    Y = df_pred.filter(regex=str(years[-1]))
    # stats from 2018-2020, used to predict stats in 2021
    Xpred = df_pred.filter(regex='|'.join(str(x) for x in list(years[1:])))
    # Make predictions
    # iterate through all stats of 2020
    for [i,col] in enumerate(Y):
        y = df_pred[col]
        reg = LinearRegression(fit_intercept=False).fit(X,y)
        # RFE default: select half of the features
        selector = RFE(reg)
        # training: use stats from 2017-2019 as X, stat from 2020 as y
        selector = selector.fit(X, y)
        #print(col,reg.score(X, y)) #check performance 
        #print(col,np.mean(cross_val_score(reg, X, y, cv=5,scoring='r2'))) #check performance
        # predict stat of 2021 using stats from 2018-2020
        preds = reg.predict(Xpred)
        df_pred[cols[i]+' '+str(2021)] = preds

    # add 2021 prediction to dataframe
    df_new = df.merge(df_pred,on='Company',suffixes=('', '_n'))
    df_new.drop(df_new.filter(regex='_n$').columns.tolist(),axis=1, inplace=True)
    df_new.loc[1482,'Sector'] = 'Unknown' #fix weird sector error
    return df_new