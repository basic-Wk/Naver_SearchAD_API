import time, random, requests, datetime, json
import pandas as pd
from pandas import DataFrame
from metrics import Naver_stat_metrics

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

# print("response status_code = {}".format(r.status_code))
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


def dateRange(i):
    day = datetime.datetime.now()-datetime.timedelta(days=i)
    start_dt = day.strftime('%Y-%m-%d')
    str = {"since": start_dt, "until": start_dt}
    result = json.dumps(str)
    # str = fr""" '{{"since": "{start_dt}", "until": "{start_dt}"}}' """
    return result, start_dt

field = json.dumps(["impCnt", "clkCnt", "ctr", "cpc", "ccnt", "salesAmt", "crto", "cpConv"])
uri = '/stats'
method = 'GET'
stat_ids = campaign_list
r = requests.get(BASE_URL + uri, params={'ids': stat_ids, 'fields': field, 'timeRange': dateRange(1)[0]}, headers=get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID))

# date_list = [dateRange(1)[1] for i in len()]

fields = r.json()['data']
df = pd.DataFrame(fields)

a = len(stat_ids)

l = [ dateRange(1)[1] for i in range(a)]

print(l)


# fields = r.json()
# print(fields)
# df = pd.DataFrame(fields)

# df.set_index('id',inplace=True)
# df.rename(Naver_stat_metrics, axis=1, inplace=True)
# df.replace(campaign_dict, inplace=True)
# df=df[['id', '노출수', '클릭수', '클릭률', '평균클릭비용', '전환수', '전환율', '총비용', '전환당비용']]
