import pandas as pd
from sklearn.preprocessing import LabelEncoder
import json

def encode_rates(df:pd.Series) -> dict[list[int]]:
    rate_string_col = df['w/rs']
    rate_dict = {'H': 3, 'M': 2, 'L': 1}
    encoded_list = []
    for rates in rate_string_col:
        attack_rate, defense_rate = rates.split('/')
        attack_encoded = rate_dict.get(attack_rate, 0)  # default to 0 if rate is not H, M, or L
        defense_encoded = rate_dict.get(defense_rate, 0)
        encoded_value = attack_encoded * 10 + defense_encoded # combine the encoded rates into a single integer
        encoded_list.append(encoded_value)
    
    return {'w/rs':encoded_list}

def unique_positions(df: pd.DataFrame) -> list:
    gian_lst = df['pos'].apply(lambda x: x.strip('[]').replace("'",'')).to_list()

    return list(set(' '.join(gian_lst).replace(',','').split(' ')))

def encode_positions(df: pd.DataFrame) -> dict[list[int]]:
    position_col_lst = []
    for i in range(len(df)):
        positions = df['pos'][i].strip('[]').replace(" '",'').replace("'",'').split(',')
        encoded_lst = [position_idxs[i] for i in positions]
        position_col_lst.append(encoded_lst)

    return {'pos':position_col_lst}

def pre_process(df: pd.DataFrame) -> list:
    df1 = pd.DataFrame()
    le = LabelEncoder()
    columns = ['name', 'foot', 'league', 'club']
    for col in columns:
        df1[col] = le.fit_transform(df[col])
    return df1[['name', 'foot', 'league', 'club']].to_dict(orient='records')

def get_numeric_data(df: pd.DataFrame) -> pd.DataFrame:
    return df.select_dtypes(include='number')

def create_final_df(df:pd.DataFrame) -> pd.DataFrame:
    final_df = pd.DataFrame()
    for func in [pre_process(df), encode_positions(df), encode_rates(df)]:
        final_df = pd.concat([final_df, pd.DataFrame(func)], axis=1)
    final_df = pd.concat([get_numeric_data(df),final_df], axis=1)
    final_df.rename(columns=column_idxs, inplace=True)
    final_df = final_df.reindex(sorted(final_df.columns), axis=1)
    return final_df

def create_positioin_players_dict(unique_positions: list) -> dict:

    orig_df = pd.read_csv('all_players_data',index_col=False)
    numeric_df = pd.read_csv('all_numeric_players_data',index_col=False)

    output = {}

    for position in unique_positions:
        indexes = orig_df['pos'].apply(lambda pos_lst: position in pos_lst)
        filtered_df = numeric_df[indexes]
        players = filtered_df.values.tolist()
        output[position] = players

    return output

df = pd.read_csv('all_players_data',index_col=False)
column_idxs = {col: i for col, i in zip(df.columns, range(len(df.columns)))}

unique_pos = unique_positions(df)
position_idxs = {pos: i for pos, i in zip(unique_pos, range(len(unique_pos)))}

final_df = create_final_df(df)

final_df.to_csv('all_numeric_players_data',index=False)

position_players_dict = create_positioin_players_dict(unique_pos)
with open("position_players_dict.json", "w") as json_file:
    json.dump(position_players_dict, json_file)

print(final_df)















    




