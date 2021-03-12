import requests
from bs4 import BeautifulSoup
import re

headers = {'Host':'www.forbes.com', 'User-Agent':'user_agent_desktop', 'Accept':'*/*', 'Accept-Encoding':'gzip, deflate, br', 'Connection':'keep-alive'}
requests.get('https://www.forbes.com/companies/icbc/?list=global2000/', headers= headers)

def extract_description(url):
    '''
    This function extracts company's name, description from the HTML page given an url of a company
    input param: string
    output param: string
    '''
    
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    page = requests.get(url, headers= headers)
    
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find_all('div', class_='profile-text')
    return results[0].find_all('span')[0].text

#Read the companies-url text file
with open('companies_list.txt','r') as f:
    urls = f.readlines() 
    
#Create a dictionary to store company - description information
description = {}
failed_url = set() #Keep tracks of url for which url scapping failed
for url in urls:
    try:
        desc = extract_description(url)
        description[url.split('/')[-3]] = desc
    except:
        failed_url.add(url)