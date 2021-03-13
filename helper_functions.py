import pandas as pd
 
def append_PCA_data(pca_filename,df):
    ''' 
    append PCA data to dataframe 
    input: pca_filename - str
    input: df - pandas dataframe to append to 
    '''
    assert isinstance(pca_filename,str)
    assert isinstance(df,pd.DataFrame)
    years = range(2008,2022) #include predicted 2021
    df_master = pd.read_csv(pca_filename) #read data from pca file
    for year in years:
        in_year = min(2019,year) #missing data for years after 2019, use 2019 data
        df_PCA = df_master[['Company','PCA_1','PCA_2','PCA_3','pca_cluster']][df_master['year']==in_year]
        df = df.join(df_PCA.set_index('Company'),on='Company',rsuffix = ' '+str(year))
    return df

def append_closest_companies(closest_filename,df):
    ''' 
    append closest companies to dataframe 
    input: closest_filename - str
    input: df - pandas dataframe to append to 
    '''
    assert isinstance(closest_filename,str)
    assert isinstance(df,pd.DataFrame)    
    
    df_closest = pd.read_csv(closest_filename) #read data from closest company file
    df['Search Company'] = df['Company'].str.lower() #convert company names to lower to match keys in dataframe
    df = df.join(df_closest.set_index('Search Company'),on='Search Company') #add closest company data
    return df

def add_ratios(df):
    ''' add ratio between stats(e.g. Assets/Profits 2021) as features in new dataset 
    not currently employed in dash app, but could be useful in the future
    input: df - pandas dataframe to append to
    '''
    assert isinstance(df,pd.DataFrame)  
    cols = ['Market Value','Sales','Profits','Assets'] #metrics to take ratios of 
    years = range(2008,2022) #include predicted 2021
    for year in years:
        for col in cols:
            for col2 in cols:
                df[col+'/'+col2+' '+str(year)] = \
                    df[col+' '+str(year)]/df[col2+ ' '+str(year)]
    return df   