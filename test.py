import time
import random
import requests
import pandas as pd
from pandas import DataFrame


import signaturehelper
import apikeys as api


def get_header(method, uri, api_key, secret_key, customer_id):
    timestamp = str(round(time.time() * 1000))
    signature = signaturehelper.Signature.generate(timestamp, method, uri, SECRET_KEY)
    return {'Content-Type': 'application/json; charset=UTF-8', 'X-Timestamp': timestamp, 'X-API-KEY': API_KEY, 'X-Customer': str(CUSTOMER_ID), 'X-Signature': signature}


BASE_URL = api.NaversearchADAPIkeys['BASE_URL']
API_KEY = api.NaversearchADAPIkeys['API_KEY']
SECRET_KEY = api.NaversearchADAPIkeys['SECRET_KEY']
CUSTOMER_ID = api.NaversearchADAPIkeys['CUSTOMER_ID']

# Adcampaign Usage Sample

# 1. GET adcampaign Usage Sample

uri = '/ncc/campaigns'
method = 'GET'
r = requests.get(BASE_URL + uri, headers=get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID))

print("response status_code = {}".format(r.status_code))
campaigns = r.json()
campaign_list = []
campaign_name = []
for i in campaigns:
    campaign = i.get('nccCampaignId')
    campaign_n = i.get('name')
    campaign_list.append(campaign)
    campaign_name.append(campaign_n)

campaign_dict = { name: value for name, value in zip(campaign_list, campaign_name)}
# Stat Usage Sample

# 1. GET Summary Report per multiple entities 

uri = '/stats'
method = 'GET'
stat_ids = campaign_list
r = requests.get(BASE_URL + uri, params={'ids': stat_ids, 'fields': '["impCnt", "clkCnt", "ctr", "cpc", "ccnt", "salesAmt", "crto", "cpConv"]', 'timeRange': '{"since":"2022-11-01","until":"2022-11-30"}'}, headers=get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID))

fields = r.json()['data'][0].keys()
df=DataFrame(None, columns=fields)

for idx in range(0,len(r.json()['data'])):
    df=pd.concat([df,DataFrame(r.json()['data'][idx],index=[idx])])

df.set_index('id',inplace=True)
df.rename({'ctr':'클릭률', 'clkCnt':'클릭수','cpc':'평균클릭비용','ccnt':'전환수','impCnt':'노출수', 'salesAmt':'총비용', 'crto':'전환율', 'cpConv':'전환당비용'}, axis=1, inplace=True)
df.rename(campaign_dict, inplace=True)
df=df[['노출수', '클릭수', '클릭률', '평균클릭비용', '전환수', '전환율', '총비용', '전환당비용']]
print(df)


# fields=r.json()['data'][0].keys()
# df=DataFrame(None,columns=fields)

# for idx in range(0,len(r.json()['data'])):
#     df=df.append(DataFrame(r.json()['data'][idx],index=[idx]))

# df.set_index('id',inplace=True)
# df.rename({'ctr':'클릭률','convAmt':'전환매출액','clkCnt':'클릭수','cpc':'평균클릭비용','ccnt':'전환수','avgRnk':'평균노출순위','impCnt':'노출수','salesAmt':'총비용'},axis=1,inplace=True)
# df=df[['노출수', '클릭수', '클릭률', '평균클릭비용', '총비용','전환수','전환매출액', '평균노출순위']]

# df

# impCnt          노출수    o
# clkCnt          클릭수    o
# ctr             클릭율    o
# cpc             평균클릭비용  o
# salesAmt        총비용    o
# ccnt            전환수    o
# crto            전환율    o
# convAmt         전환매출액
# ror             광고수익률(전환매출/총비용)
# cpConv          전환당비용(총비용/전환수) o
# avgRnk          평균노출순위
# pcNxAvgRnk      PC 통검 평균노출순위
# mblNxAvgRnk     모바일 통검 평균노출순위
# recentAvgRnk    최근통검 평균노출순위
# viewCnt         동영상조회수