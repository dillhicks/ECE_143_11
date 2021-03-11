import wikipedia
import pandas as pd
from tqdm import tqdm
from os.path import join
import os
import argparse


def get_Descriptions(path, outpath):
    '''
    run wikipedia_scrape.py -h for help

    gets Descriptions for Forbes dataset csvs in a path

    path - input path containing only forbes dataset csvs
    type: str (path)

    path - output path to put scraped csvs
    type: str (path)

   
    '''

    for filename in os.listdir(path):
        #making sure all files are csvs 
        assert filename.endswith(".csv")
        assert filename.startswith("Forbes Global 2000")

        #getting description
        if not os.path.exists(join(path, "updated" + filename)):
            print(filename)
            data = pd.read_csv(join(path,filename)) 
            data["description"] = ""

            #iterating through rows of csv
            for index, row in tqdm(data.iterrows(), total=data.shape[0]):
                term = wikipedia.search(row["Company"] + " company", results=1)
                try:
                    data.loc[index, 'description'] = wikipedia.summary(term, auto_suggest=False)
                except:
                    #If wikipedia can't find the company
                    data.loc[index, 'description'] = "NEEDS_MANUAL_SUMMARY"
            
            data.to_csv(join(outpath, "updated" + filename))





if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get wikipedia descriptions for forbes dataset.')
    parser.add_argument('--in_path', help='path of Forbes dataset')
    parser.add_argument('--out_path', help='output path')

    args = parser.parse_args()
    get_Descriptions(args.in_path, args.out_path)


