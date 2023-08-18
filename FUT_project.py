import requests
import csv
import re
import pandas as pd
import numpy as np
from pandas.errors import ParserError                            
import random
from bs4 import BeautifulSoup
from sklearn.preprocessing import LabelEncoder
import os

# from urllib.parse import urlencode
# from urllib.request import Request, urlopen
# import json
# from requests import ReadTimeout


API_KEY = '1a3957db-ee0c-475e-9cfc-77a4ac059301'
def get_headers_list():
    response = requests.get('http://headers.scrapeops.io/v1/browser-headers?api_key=' + API_KEY)
    json_response = response.json()
    return json_response.get('result', [])

def scrape() -> pd.DataFrame:
    df = pd.DataFrame()
    flags = []
    res_ok = True
    i=0
    cols =''
    while res_ok:
        try:
            res = requests.get(f'http://www.futwiz.com/en/fifa23/players?page={i}', headers=random.choice(get_headers_list()), timeout=30)
            soup = BeautifulSoup(res.text, 'html.parser')
            res_ok = res.ok
        except requests.HTTPError as e:
            print('Error', e)
            print(f'status code: {res.status_code}')
            break
        try:
            table = pd.read_html(res.text, attrs={'class':'table results playersearchresults'},  displayed_only=False)[0]
            table = table.iloc[:, 1:]
            if i == 0: #the first row of the table contains the names of the columns
                cols = [*table.iloc[0]]
                # i = 830

            if table.shape[0] <= 1:
                print('break')
                break
            else:
                table = table[1:]
                print('alive')
        except ValueError as e:
            print('Error: ', e)
            temp = df.shape[0] - len(flags)
            if temp > 0:
                x=2
            # df = df[:-temp]
            
            continue
        df = pd.concat([df, table])
        # print(df)

        lst = soup.find_all('p', class_ = 'team') # get all the 'p' web element containing the flags
        flags += [x.a.img['src'] for x in lst] # get all the links of the flags
        i+=1
        print(df.shape)

    le = LabelEncoder()
    flags = le.fit_transform(flags) # ennumarate the links
    df.columns = [x.strip() for x in cols] # set the columns names to cols
    df['Nationality'] = flags
    
    return df 


def get_flags(df: pd.DataFrame, iterations) -> None:
    flags = []
    res_ok = True
    i=0
    while i <= iterations:
        try:
            res = requests.get(f'http://www.futwiz.com/en/fifa23/players?page={i}', headers=random.choice(get_headers_list()), timeout=30)
            soup = BeautifulSoup(res.text, 'html.parser')
            res_ok = res.ok
        except requests.HTTPError as e:
            print('Error', e)
            print(f'status code: {res.status_code}')
            break

        lst = soup.find_all('p', class_ = 'team') # get all the 'p' web element containing the flags
        flags += [x.a.img['src'] for x in lst] # get all the links of the flags
        i+=1
        if i % 20 == 0:
            print(f'iteration: {i}, length = {len(flags)}')
    le = LabelEncoder()
    flags = le.fit_transform(flags) # ennumarate the links
    df['Nationality'] = flags

def format_player(df: pd.DataFrame) -> None:
    # df.reset_index(drop=True, inplace=True)
    player_names = []
    club_names = []
    clubs = sorted(get_clubs())

    df['League'] = df['Player'].apply(lambda x:x.split('|')[1])
    df['Player'] = df['Player'].apply(lambda x: x.split('|')[0].strip())
    
    for _, row in df.iterrows():
        max_substring = ''
        for substring in clubs:
            if row['Player'].endswith(substring) and len(substring) > len(max_substring):
                max_substring = substring
                
        player_names.append(row['Player'].replace(max_substring, '').strip())
        club_names.append(max_substring)
        if max_substring == '':
            print(row['Player']) # for debuging
    x = df['Player']
    df['Club'] = club_names
    df['Player'] = player_names
    # df.drop('Unnamed: 0', axis=1, inplace=True)
    
def get_clubs() -> list:
    res = requests.get('https://www.futwiz.com/en/fifa23/clubs')
    # print(res.ok)
    soup = BeautifulSoup(res.text, 'html.parser')
    lst = soup.find_all('h5')
    clubs = [x.a.contents[0] for x in lst]
    # print(len(clubs))
    clubs = set([x.strip() for x in clubs])
    # print(len(clubs))
    
    return clubs

def convert_stats_to_int(df: pd.DataFrame) -> None:
    stats = ['PAC','SHO','PAS','DRI','DEF','PHY']
    df['POS'] = df['POS'].apply(lambda x: x.split())
    for stat in stats:
        df[stat] = df[stat].apply(lambda x: re.split(r'\s+', x)[1])

def get_data() -> pd.DataFrame:
    df = scrape()
    # get_flags(df, iterations)
    format_player(df)
    convert_stats_to_int(df)
    return df


''''''''''''''''''''''''''''''''''''



if __name__ == '__main__':
    
 
    # result_df = get_data()
    # result_df.to_csv('all_players_dat a',index=False)
    # print(os.getcwd())
    data = pd.read_csv('all_players_data', index_col=False)
   
   
    







    
    
    


