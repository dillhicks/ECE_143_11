import pandas as pd
 
def append_PCA_data(pca_path,years,df):    
    df_master = pd.read_csv(pca_path) #read data from pca file
    for year in years:
        in_year = min(2019,year) #missing data for years after 2019, use 2019 data
        df_PCA = df_master[['Company','PCA_1','PCA_2','PCA_3','pca_cluster']][df_master['year']==in_year]
        df = df.join(df_PCA.set_index('Company'),on='Company',rsuffix = ' '+str(year))
    return df

def append_closest_companies(closest_path,df):
    df_closest = pd.read_csv(closest_path) #read data from closest company file
    df['Search Company'] = df['Company'].str.lower()
    df = df.join(df_closest.set_index('Search Company'),on='Search Company')
    return df

def add_ratios(df,years,cols):
    # add ratio between stats(e.g. Assets/Profits 2021) as features in new dataset
    # not employed in dash app, but could be useful in the future    
    for year in years:
        for col in cols:
            for col2 in cols:
                df[col+'/'+col2+' '+str(year)] = \
                    df[col+' '+str(year)]/df[col2+ ' '+str(year)]
    return df   