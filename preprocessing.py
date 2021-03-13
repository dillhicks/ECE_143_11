import pandas as pd
# package to convert and match country names between different classifications and between different naming versions
import country_converter as coco
    
def preprocess_data(folder_path):
    ''' 
    Read and merge all data files, add ISO codes for world map
    :input param: folder_path 
    :input type: str
    '''
   
    assert isinstance(folder_path,str)
    cols = ['Market Value','Sales','Profits','Assets','Rank'] #metrics of interest
    years = range(2008,2021) #years to include
    default_cols = ['Company','Country','Industry','Sector','PCA_1','PCA_2','PCA_3','pca_cluster'] #default columns in df
    df = pd.DataFrame(columns=default_cols) 

    for year in years:
        # raw data for the specific year
        temp = pd.read_csv(folder_path+'Forbes Global 2000 - ' + str(year) +'.csv')
        for col in temp.columns:
            # if company name is 'Company/ABC' or 'Company(ABC)'
            # change the name to 'Company'
            c = col.split(' (')[0];
            c = c.split('/')[0];
            temp.rename(columns={col:c}, inplace=True)
            # rename 'revenue' to 'sales'
            if col == 'Revenue':
                c = 'Sales'
                temp.rename(columns={col:c}, inplace=True)
            # change str '$2.1B' to int 2.1 for all 2020 stats
            # if unit is 'M', convert to 'B' by dividing it by 1000
            if year == 2020 and c in cols and c != "Rank":
                for index,row in temp[c].items():
                    if row[-1] == 'B':    # billion unit
                        val = float(row[1:-1].replace(',',''))
                        temp.at[index,c] = val
                    elif row[-1] == 'M':                    # million unit
                        val = float(row[1:-1].replace(',',''))/1000
                        temp.at[index,c] = val
                temp[c] = temp[c].astype(float)
           
            # if column is among 'Market Value','Sales','Profits','Assets','Rank'
            # add year to its name e.g.'Market value 2008'
            if c in cols or c=='Rank':
                cy = c+ ' '+str(year)
                temp.rename(columns={c:cy}, inplace=True)
            # if column is among 'Company','Country','Industry'
            if col in default_cols[1:len(default_cols)]:
                temp[col].update(df.pop(col))
        # merge df's 'Company' column with temp's 'Company' column
        df = df.merge(temp,on = 'Company',how='outer')

    df = df.rename(columns={'Country_y':'Country'})
    # if industry is 'na', fill it with 'unknown'
    df["Industry"] = df["Industry"].fillna("Unknown")
    df['Sector'] = df['Sector'].fillna('unknown')
    # only pick non-NA entries for 'country'
    df = df[df["Country"].notna()]
    df["ISO Code"] = coco.convert(names=df["Country"].tolist(), to='ISO3')
    # remove duplicate columns of "Continent_y"
    # caused by combining same company data from different years
    temp = df.filter(like = "Continent_y")
    df["Continent"] = temp.iloc[:,0] #not used currently in dash, but may be used later
    
    return df