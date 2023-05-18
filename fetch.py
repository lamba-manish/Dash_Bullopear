import pymongo
import time
import datetime
import flask
from flask import Flask, render_template
import json
import requests
from pymongo import MongoClient
import plotly.graph_objects as go
import plotly.offline as offline
import plotly.express as px
import pandas as pd
import MySQLdb
import sshtunnel
import re
import ast

class Fetch():
    def __init__(self, security_name, expiry=None):
        # self.security_type = security_type
        self.expiry=expiry
        self.security_name = security_name
        self.spot_price = []
        self.expiry_date = []
        self.fetched_at_time = []
        self.strikes_list = []
        self.near_atm_strikes = []
        self.atm_strike = []
        self.call_oi = []

        self.call_price=[]
        self.put_price=[]

        self.put_oi = []
        self.call_change_oi = []
        self.put_change_oi = []
        self.call_volume = []
        self.put_volume = []
        self.atm_strike = []
        with open('data_mapper.json', 'r') as file:
            self.security_dict=json.load(file)
        
        self.atm_slicer = self.security_dict[security_name]["slicer"]
        self.lot_size = self.security_dict[security_name]["lot_size"]
        self.headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36','accept-language': 'en,gu;q=0.9,hi;q=0.8','accept-encoding': 'gzip, deflate, br'}
        self.fetched_data = {} 
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client[f"{self.security_name}_daily_oi"]
        self.collection = self.db[f"{self.security_name}_oi_collection"]
        self.last_fetched_document = self.collection.find().sort("_id", -1).limit(1)
        self.fetched_data = [doc for doc in self.last_fetched_document][0]

        # sshtunnel.SSH_TIMEOUT = 5.0
        # sshtunnel.TUNNEL_TIMEOUT = 5.0
        # with sshtunnel.SSHTunnelForwarder(
        #     ('ssh.pythonanywhere.com'),
        #     ssh_username='Bullopear', ssh_password='pythonpassword',
        #     remote_bind_address=('Bullopear.mysql.pythonanywhere-services.com', 3306)
        # ) as tunnel:
        #     connection = MySQLdb.connect(
        #      user='Bullopear',
        #      passwd='dbpassword',
        #     host='127.0.0.1', port=tunnel.local_bind_port,
        #     db='Bullopear$DAILYOI_change',
        # )
        #     cursor=connection.cursor()
        #     query = f"SELECT records, filtered FROM {self.security_name.upper()} WHERE date = (SELECT MAX(date) FROM {self.security_name.upper()} ORDER BY filtered DESC LIMIT 1);"
        #     cursor.execute(query)
        #     result = cursor.fetchall()
        #     cursor.close()
        #     records=json.loads(result[0][0])
        #     filtered=json.loads(result[0][1])
        #     result_dict={'records':records, 'filtered':filtered}
        #     self.fetched_data=result_dict
        #     self.time = self.fetched_data['records']['timestamp']

        self.fetch_For_Security()

    def get_expiry_date_commodity(self, input='CRUDEOIL'):
        url = 'https://www.mcxindia.com/market-data/option-chain'
        response = requests.get(url)
        pattern = re.compile(r'var vTick=\[(.*?)\];', re.DOTALL)
        match = pattern.search(response.text)
        if match:
            json_str = match.group(1)
            json_str = json_str[:json_str.rfind('}')+1]
        else:
            print('JSON object not found in HTML content')
            exit()
        data = ast.literal_eval(json_str)
        crudeoil_expiry=[]
        naturalgas_expiry=[]
        for item in data:
            if item['Symbol']=='CRUDEOIL':
                crudeoil_expiry.append(item['ExpiryDate'])
            elif item['Symbol']=='NATURALGAS':
                naturalgas_expiry.append(item['ExpiryDate'])
        if input.upper()=='CRUDEOIL':
            return crudeoil_expiry
        if input.upper()=='NATURALGAS':
            return naturalgas_expiry

    def return_expiry_dates(self):
        if self.security_name.upper()=='CRUDEOIL':
            return self.get_expiry_date_commodity()
        elif self.security_name.upper()=='NATURALGAS':
            return self.get_expiry_date_commodity('NATURALGAS')
        elif self.security_name.upper() in ['SENSEX', 'BANKEX', 'SX50']:
            bse_mapper={'IO':{'SENSEX':1, 'BANKEX':12, 'SX50':47}}
            expiry_url=f'https://api.bseindia.com/BseIndiaAPI/api/ddlExpiry/w?ProductType=IO&scrip_cd={bse_mapper["IO"][self.security_name]}'
            base_url='https://www.bseindia.com'
            sess=requests.Session()
            response=sess.get(url=base_url, headers=self.headers, timeout=10)
            cookies=response.cookies
            expiry_dates=sess.get(url=expiry_url, headers=self.headers, cookies=cookies, timeout=10).json()['Table']
            expiry_date_list=[item['eXPIRY'] for item in expiry_dates]
            return expiry_date_list

        else:
            return self.fetched_data['records']['expiryDates']
        
    def near_Atm_Strikes(self, strikes_list, atm_strike, n):
        index = self.strikes_list.index(self.atm_strike)
        start = max(0, index-n)
        before = self.strikes_list[start:index]
        end = min(len(self.strikes_list), index + n+1)
        after = self.strikes_list[index+1:end]
        self.near_atm_strikes = before + [self.atm_strike] + after
        return self.near_atm_strikes
    def fetch_For_Security(self):
        # if self.security_type.lower() == "indices":
        #     self.fetch_For_Indices_And_Currency(self.security_name)
        # elif self.security_type.lower() == "equities":
        #     self.fetch_For_Equities(self.security_name)
        # elif self.security_type.lower() == "currency":
        #     self.fetch_For_Indices_And_Currency(self.security_name)
        # elif self.security_type.lower() == "commodity":
        #     self.fetch_For_Commodities(self.security_name)
        # else:
        #     return "Security not Found"
        if self.security_name.lower() in ['usdinr','nifty','banknifty','finnifty', 'midcpnifty']:
            self.fetch_For_Indices_And_Currency(self.security_name)
        elif self.security_name.lower() in ['crudeoil', 'naturalgas']:
            self.fetch_For_Commodities(self.security_name)
        elif self.security_name.lower() in ['sensex', 'bankex', 'sx50']:
            self.fetch_for_bse_options(self.security_name)
        else:
            self.fetch_For_Indices_And_Currency(self.security_name)

    def fetch_for_bse_options(self, security_name):
        # bse_mapper={'IO':{'SENSEX':1, 'BANKEX':12, 'SX50':47}}
        # expiry_url=f'https://api.bseindia.com/BseIndiaAPI/api/ddlExpiry/w?ProductType=IO&scrip_cd={bse_mapper["IO"][self.security_name]}'
        # base_url='https://www.bseindia.com'
        # sess=requests.Session()
        # response=sess.get(url=base_url, headers=self.headers, timeout=10)
        # cookies=response.cookies
        # expiry_dates=sess.get(url=expiry_url, headers=self.headers, cookies=cookies, timeout=10)
        # expiry_date=expiry_dates.json()['Table'][0]['eXPIRY']
        # formatted_expiry_date=expiry_date[0:2]+'+'+expiry_date[3:6]+'+'+expiry_date[7:]
        # index_url=f'https://api.bseindia.com/BseIndiaAPI/api/DerivOptionChain/w?Expiry={formatted_expiry_date}&ProductType=IO&scrip_cd={bse_mapper["IO"][self.security_name]}'
        # output=sess.get(url=index_url, headers=self.headers, cookies=cookies, timeout=10)
        # data=output.json()
        data=self.fetched_data
        table=data['Table']
        self.strikes_list=[item['Strike_Price'] for item in table]
        self.expiry_date=self.return_expiry_dates()[0]
        self.spot_price=table[0]['UlaValue']
        self.fetched_time=data['ASON'][0]['DT_TM']
        for item in self.strikes_list:
            if abs(item-float(self.spot_price))<self.atm_slicer:
                self.atm_strike = item
        self.near_Atm_Strikes=self.near_Atm_Strikes(self.strikes_list, self.atm_strike, 12)
        self.call_oi=[item['C_Open_Interest'] for item in table]
        self.put_oi=[item['Open_Interest'] for item in table]
        # self.call_change_oi=[x*self.security_dict[self.security_name]['lot_size'] for x in self.call_oi]
        # self.put_change_oi = [x*self.security_dict[self.security_name]['lot_size'] for x in self.put_oi]
        self.call_change_oi=self.call_oi
        self.put_change_oi=self.put_oi

    def fetch_For_Indices_And_Currency(self, security_name):
        self.strikes_list = self.fetched_data['records']['strikePrices']
        expiry_date_index=self.return_expiry_dates().index(self.expiry) if self.expiry else 0
        self.expiry_date = self.fetched_data['records']['expiryDates'][expiry_date_index]
        self.spot_price = self.fetched_data['records']['underlyingValue']
        self.fetched_time = self.fetched_data['records']['timestamp']
        for item in self.strikes_list:
            if abs(item - float(self.spot_price)) < self.atm_slicer:
                self.atm_strike = item
        if self.security_name == "USDINR":
            self.near_atm_strikes = self.near_Atm_Strikes(self.strikes_list, self.atm_strike,7)
        else:
            self.near_atm_strikes = self.near_Atm_Strikes(self.strikes_list, self.atm_strike, 12)
        for item in self.fetched_data["records"]["data"]:
            if item["strikePrice"] in self.near_atm_strikes:
                if item["expiryDate"] == self.expiry_date:
                    if "CE" in item.keys():
                        self.call_oi.append(item["CE"]["openInterest"])
                        self.call_change_oi.append(item["CE"]["changeinOpenInterest"])
                        self.call_volume.append(item["CE"]["totalTradedVolume"])

                        self.call_price.append(item["CE"]["lastPrice"])

                    else:
                        self.call_oi.append(0)
                        self.call_change_oi.append(0)
                        self.call_volume.append(0)

                        self.call_price.append(0)

                    if "PE" in item.keys():
                        self.put_oi.append(item["PE"]["openInterest"])
                        self.put_change_oi.append(item["PE"]["changeinOpenInterest"])
                        self.put_volume.append(item['PE']['totalTradedVolume'])

                        self.put_price.append(item["PE"]["lastPrice"])

                    else:
                        self.put_oi.append(0)
                        self.put_change_oi.append(0)
                        self.put_volume.append(0)
                else:
                    pass
            else:
                pass
        call_oi_calculation = [x*self.security_dict[self.security_name]['lot_size'] for x in self.call_oi]
        put_oi_calculation = [x*self.security_dict[self.security_name]['lot_size'] for x in self.put_oi]
        call_change_oi_calculation = [x*self.security_dict[self.security_name]['lot_size'] for x in self.call_change_oi]
        put_change_oi_calculation = [x*self.security_dict[self.security_name]['lot_size'] for x in self.put_change_oi]
        self.call_oi = call_oi_calculation
        self.put_oi = put_oi_calculation
        self.call_change_oi = call_change_oi_calculation
        self.put_change_oi = put_change_oi_calculation
        
        
    def fetch_For_Equities(self, security_name):
        pass
#     def fetch_For_Currency(self, security_name):
#         self.strikes_list = self.fetched_data["records"]["strikePrices"]
#         self.expiry_date = self.fetched_data["records"]["expiryDates"][0]
#         self.spot_price = self.fetched_data["records"]["underlyingValue"]
#         for item in self.strikes_list:
#             if abs(item - float(self.spot_price)) < self.atm_slicer:
#                 self.atm_strike = item
#         self.near_atm_strikes = self.near_Atm_Strikes(self.strikes_list, self.atm_strike, 5)
#         for item in self.fetched_data["filtered"]["data"]:
#             if item["strikePrice"] in self.near_atm_strikes:
#                 if item["expiryDate"]==self.expiry_date:
#                     if "CE" in item.keys():
#                         self.call_oi.append(item["CE"]["openInterest"])
#                         self.call_change_oi.append(item["CE"]["changeinOpenInterest"])
#                         self.call_volume.append(item["CE"]["totalTradedVolume"])
#                     else:
#                         self.call_oi.append(0)
#                         self.call_change_oi.append(0)
#                         self.call_volume.append(0)
#                     if "PE" in item.keys():
#                         self.put_oi.append(item["PE"]["openInterest"])
#                         self.put_change_oi.append(item["PE"]["changeinOpenInterest"])
#                         self.put_volume.append(item['PE']['totalTradedVolume'])
#                     else:
#                         self.put_oi.append(0)
#                         self.put_change_oi.append(0)
#                         self.put_volume(0)
#                 else:
#                     pass
#             else:
#                 pass
    
    
    def fetch_For_Commodities(self, security_name):
        self.spot_price = self.fetched_data['d']['Data'][0]['UnderlyingValue']
        timefetched = int(self.fetched_data['d']['Summary']['AsOn'][6:-5])
        self.fetched_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timefetched))
        self.expiry_date = self.get_expiry_date_commodity()[0] if security_name.upper()=='CRUDEOIL' else self.get_expiry_date_commodity('NATURALGAS')[1]
        for item in range(len(self.fetched_data['d']['Data'])):
            self.strikes_list.append(self.fetched_data['d']['Data'][item]['CE_StrikePrice'])
        for item in self.strikes_list:
            if abs(item - float(self.spot_price)) < self.atm_slicer:
                self.atm_strike = item
        self.near_atm_strikes = self.near_Atm_Strikes(self.strikes_list, self.atm_strike, 12)
        for item in self.fetched_data['d']['Data']:
            if item['CE_StrikePrice'] in self.near_atm_strikes:
                self.call_oi.append(item['CE_OpenInterest'])
                self.put_oi.append(item['PE_OpenInterest'])
                self.call_change_oi.append(item['CE_ChangeInOI'])
                self.put_change_oi.append(item['PE_ChangeInOI'])
                self.call_volume.append(item['CE_Volume'])
                self.put_volume.append(item['PE_Volume'])
            else:
                pass

                                    
                                    