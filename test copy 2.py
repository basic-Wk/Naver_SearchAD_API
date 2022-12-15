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

def dateRange(i):
    day = datetime.datetime.now()-datetime.timedelta(days=i)
    start_dt = day.strftime('%Y-%m-%d')
    str = {"since": start_dt, "until": start_dt}
    result = json.dumps(str)
    # str = fr""" '{{"since": "{start_dt}", "until": "{start_dt}"}}' """
    return result, start_dt

# Adcampaign Usage Sample

# 1. GET adcampaign Usage Sample
def get_df():

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
    field = ["impCnt", "clkCnt", "ctr", "cpc", "ccnt", "salesAmt", "crto", "cpConv"]
    field_json = json.dumps(field)
    dfs = pd.DataFrame()
    date_dfs = pd.DataFrame()

    for i in range(1,3):
        uri = '/stats'
        method = 'GET'
        stat_ids = campaign_list
        r = requests.get(BASE_URL + uri, params={'ids': stat_ids, 'fields': field_json, 'timeRange': dateRange(i)[0]}, headers=get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID))
        len_campaign = len(stat_ids)
        date_list = [ dateRange(i)[1] for j in range(len_campaign)]
        date_df = pd.DataFrame({'date' : date_list}) 
        fields = r.json()['data']
        df = pd.DataFrame(fields)
        dfs = pd.concat([dfs, df], ignore_index=True)
        date_dfs = pd.concat([date_dfs, date_df], ignore_index=True)

    dfs = pd.concat([dfs, date_dfs], axis=1)
    df.set_index('id',inplace=True)
    dfs.rename(Naver_stat_metrics, axis=1, inplace=True)
    dfs.replace(campaign_dict, inplace=True)
    dfs=dfs[['id', '노출수', '클릭수', '클릭률', '평균클릭비용', '전환수', '전환율', '총비용', '전환당비용', 'date']]
    return dfs