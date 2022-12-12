import time
import random
import requests
import pandas as pd
from pandas import DataFrame


import signaturehelper


def get_header(method, uri, api_key, secret_key, customer_id):
    timestamp = str(round(time.time() * 1000))
    signature = signaturehelper.Signature.generate(timestamp, method, uri, SECRET_KEY)
    return {'Content-Type': 'application/json; charset=UTF-8', 'X-Timestamp': timestamp, 'X-API-KEY': API_KEY, 'X-Customer': str(CUSTOMER_ID), 'X-Signature': signature}


BASE_URL = 'https://api.searchad.naver.com'
API_KEY = '0100000000a6384c9ce78eb2dd7b3fd3b79438bd9d302370ce011949aa223bc1ed58f88cfe'
SECRET_KEY = 'AQAAAACmOEyc546y3Xs/07eUOL2dpD+lcEfIYk5FX5fCYEFEhA=='
CUSTOMER_ID = '2468931'

# Adcampaign Usage Sample

# 1. GET adcampaign Usage Sample

uri = '/ncc/campaigns'
method = 'GET'
r = requests.get(BASE_URL + uri, headers=get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID))

print("response status_code = {}".format(r.status_code))
campaigns = r.json()
campaign_list = []
for i in campaigns:
    campaign = i.get('nccCampaignId')
    campaign_list.append(campaign)

# Stat Usage Sample

# 1. GET Summary Report per multiple entities 

uri = '/stats'
method = 'GET'
#stat_ids = [target_adgroup['nccCampaignId'], target_adgroup['nccAdgroupId']]
stat_ids = campaign_list
r = requests.get(BASE_URL + uri, params={'ids': stat_ids, 'fields': '["impCnt", "clkCnt", "ctr", "cpc", "ccnt"]', 'timeRange': '{"since":"2022-11-01","until":"2022-11-30"}'}, headers=get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID))

fields=r.json()['data'][0].keys()
df=DataFrame(None,columns=fields)

for idx in range(0,len(r.json()['data'])):
    df=df.append(DataFrame(r.json()['data'][idx],index=[idx]))

df.set_index('id',inplace=True)
df.rename({'ctr':'클릭률', 'clkCnt':'클릭수','cpc':'평균클릭비용','ccnt':'전환수','impCnt':'노출수'},axis=1,inplace=True)
df=df[['노출수', '클릭수', '클릭률', '평균클릭비용', '전환수']]
print(df)


# fields=r.json()['data'][0].keys()
# df=DataFrame(None,columns=fields)

# for idx in range(0,len(r.json()['data'])):
#     df=df.append(DataFrame(r.json()['data'][idx],index=[idx]))

# df.set_index('id',inplace=True)
# df.rename({'ctr':'클릭률','convAmt':'전환매출액','clkCnt':'클릭수','cpc':'평균클릭비용','ccnt':'전환수','avgRnk':'평균노출순위','impCnt':'노출수','salesAmt':'총비용'},axis=1,inplace=True)
# df=df[['노출수', '클릭수', '클릭률', '평균클릭비용', '총비용','전환수','전환매출액', '평균노출순위']]

# df