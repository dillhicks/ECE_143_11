# ECE 143 Team 11: Business Analytics Dashboard

Team Members:

James Long, John Babbitt, Christine Lind, Dillon Hicks, Nilesh Pandey


# Usage and Modules Used:

To just use the dash app, run dash_app.ipynb. It will load preprocessed data from pickle in pickles folder. To redo preprocessing, follow steps below.  

All modules below can be installed with conda except for those marked with a *

### Scraping:

In order to scrape descriptions for the forbes datasets, ensure that you have a folder containing the forbes datasets and an empty folder where the scraped datasets will be written. Then, giving the paths to these two folders relative to the script, run the python file with the following arguments:

```python
python scraping.py --in_path “input path” --out_path “output path”
```

```python
#Dependencies 
pandas
wikipedia*
tqdm
```


### Vectorizing:


In order to run the vectorization and to add features to a master dataset, ensure that the scraped datasets are in the `scraped` folder. Then, run the notebook in its entirety. 

The start of the notebook contains helper functions for finding the proper clusters for k-means via the elbow method, and functions to create vectors and add final features to the data. It also includes sample visualizations for the clustering for fasttext and TF-IDF vectors

The master scraped and vectorized .csv and .pkl for importing should be written to the same directory. 


```python
#Dependencies 
numpy
pandas
sklearn
nltk
matplotlib
sister*
plotly
tqdm
```

### Closest Company Predictions:
Import the closest_company.py python script. The python function “k_closest(company,k)” takes two input parameters, query company (string format) and k, the number of closest companies (int format) and returns the k closest companies, their sector and their revenue.

Eg. 
```python
print(k_closest(apple,5))
```

Sample output:

```python
[('Amazon', 'Consumer Discretionary', 232.887),
 ('McKesson', 'Health Care', 213.518),
 ('Nomura', 'Health Care', 141.935),
 ('Microsoft', 'Information Technology', 118.224),
 ('Dell Technologies', 'Information Technology', 90.396)]
```

```
#Dependencies 
json
numpy
pandas
pickle5
```

### Preprocessing and Future Predictions:

This is done in the final_dataframe_for_dash notebook, by calling functions in the following files: 

#### Preprocessing: 
Reads csv data from each year in the dataset folder, reformats the data and adds ISO codes to each country. 

#### Predictions:
Performs predictions for ‘Market Value’, ’Assets’, ‘Profts’, ‘Sales’ and ‘Rank’ for 2021 using a linear regression model and appends predictions to the dataframe. 

#### Helper functions: 
Appends PCA and closest company information as well as ratios of above metrics to the dataframe used in dash visualization. 

```
#Dependencies 
pandas
country_converter
sklearn
```


### Dash App:

Inputs: 

    - Year (slider): 

           The year of the Forbes 2000 list (2008-2020, with 2021's prediction)
           
    - Metric (radio button): 
    
           The metric used (Sales, Assets, Profits, Market Value)
           
    - Country (dropdown): 
    
           The country which companies on the Forbes 2000 list affiliate to
    - Sector (dropdown): 
    
           The list of sectors which all of the companies in the entire database belong to
          
    - Company (dropdown):
    
           The specific company to look at

Outputs:

    - World map: 
    
           Heat map displaying the average value of the selected metric (unit Billion dollar USD) in the selected year
           
    - Tab 'Country': 
    
           Pie-chart of the total sum of selected metric each sector has, within all the sectors present in the selected country and year
           
           Bar plot of total sum of selected metric of all sectors in the selected country across all the years
           
            If no country is selected, data from all countries are included.
           
    - Tab 'Sector': 
    
            Bar plot of total sum of selected metric of all industries in the selected sector, country and year
            
            Bar plot of total sum of selected metric of all industries in the selected sector and country across all the years
            
            If no country is selected, data from all sectors are included.

    - Tab 'Company': 

           Bar plot of the four metrics of the selected company along with its top-4 closest companies (or less) in the dataset, in the selected year

           Bar plot of the four metrics of the selected company along with its top-4 closest companies (or less) in the dataset, across all the years
           
    - Tab 'Cluster': 
    
           The specific company to look at
           

```
#Dependencies 
dash
plotly
```

For proper formating of the jupyter notebooks, view the nbviewer below:
https://nbviewer.jupyter.org/github/dillhicks/ECE_143_11/blob/main/Vectorize.ipynb
https://nbviewer.jupyter.org/github/dillhicks/ECE_143_11/blob/main/examples/example_plot.ipynb

