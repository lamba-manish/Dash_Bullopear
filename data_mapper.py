import pandas as pd
import re
import json
url='https://archives.nseindia.com/content/fo/fo_mktlots.csv'
df=pd.read_csv(url)
fno_list_temp=list(df.iloc[5:,1])
df_temp=df.iloc[5:,1:3]
df_temp.columns=['symbol', 'lot_size']
# print(df_temp)
fno_list=[]
# data_mapper={}

# print(data_mapper)
# result_dict = {}
# for item in df_temp['symbol']:
#     item_stripped = item.strip().replace('&', '%26')
#     item_value = df_temp.loc[df_temp['symbol'] == item, 'lot_size'].iloc[0]
#     item_value_str = item_value.strip()
#     item_dict = {'url': item_stripped, 'db_name': re.sub(r'[^a-zA-Z0-9\s]', '', item_stripped), 'lot_size': int(item_value_str), 'slicer':None}
#     result_dict[item.strip()] = item_dict

# print(result_dict)

# with open('data_mapper.json', 'w') as f:
#     json.dump(result_dict, f)

# print('Dictionary saved as JSON file')


import json



with open('modified_data_mapper.json', 'r') as file:
    data=json.load(file)

print(type(data))
print(type(data['NIFTY']))
print(type(data['NIFTY']['lot_size']))

