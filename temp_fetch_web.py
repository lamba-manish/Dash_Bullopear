import requests
import time
import os
import sys
import json
from datetime import datetime, date
MAX_RETRIES = 5
mcx_headers  = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Content-Length": "45",
    "Content-Type": "application/json",
    "Dnt": "1",
    "Host": "www.mcxindia.com",
    "Origin": "https://www.mcxindia.com",
    "Pragma": "no-cache",
    "Referer": "https://www.mcxindia.com/market-data/option-chain",
    "Sec-Ch-Ua": '"Microsoft Edge";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
    "X-Requested-With": "XMLHttpRequest"
}

nse_headers = {
    "authority": "www.nseindia.com",
    "method": "GET",
    "path": "/api/option-chain-indices?symbol=BANKNIFTY",
    "scheme": "https",
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
    "Cache-Control": "no-cache",
    "Dnt": "1",
    "Pragma": "no-cache",
    "Referer": "https://www.nseindia.com/option-chain",
    "Sec-Ch-Ua": '"Microsoft Edge";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
}


bse_headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
    "Origin": "https://www.bseindia.com",
    "Referer": "https://www.bseindia.com/",
    "Sec-Ch-Ua": '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"macOS"',
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}

def temp_set_cookies(index_name='NSE'):
        if index_name == 'NSE':
            url = 'https://www.nseindia.com'
            response = temp_fetch(url=url, headers=nse_headers)
            if response is not None and response.status_code == 200:
                cookies = dict(response.cookies)
                return cookies
            else:
                 return -1
            
def temp_fetch(url, headers, cookies=None, retries = MAX_RETRIES):
        session = requests.Session()
        response = None
        for _ in range(retries):
            try:
                response = session.get(url, headers=headers, cookies=cookies, timeout=2)
                if response.status_code == 200:
                    return response
            except Exception as e:
                print(f'Failed to fetch, {str(e)}')
        if response is None:
            print(f'Failed to fetch data after all retries')

def temp_fetch_call(security_name):
     if security_name.upper() in ['NIFTY', 'BANKNIFTY', 'FINNIFTY', 'MIDCPNIFTY']:
          url= f'https://www.nseindia.com/api/option-chain-indices?symbol={security_name.upper()}'
          cookies = temp_set_cookies()
          data = temp_fetch(url, headers=nse_headers, cookies=cookies)
          temp_fetched_data = data.json()
          return temp_fetched_data
     elif security_name.upper() == 'USDINR':
          url = 'https://www.nseindia.com/api/option-chain-currency?symbol=USDINR'
          cookies = temp_set_cookies()
          data = temp_fetch(url, headers=nse_headers, cookies=cookies)
          temp_fetched_data = data.json()
          return temp_fetched_data
     elif security_name.upper() in ['SENSEX', 'BANKEX', 'SX50']:
          pass
     elif security_name.upper() in ['CRUDEOIL', 'NATURALGAS']:
          pass
     else:
          url = f'https://www.nseindia.com/api/option-chain-equities?symbol={security_name.upper()}'
          cookies=temp_set_cookies()
          data = temp_fetch(url, headers=nse_headers, cookies=cookies)
          temp_fetched_data = data.json()
          return temp_fetched_data


