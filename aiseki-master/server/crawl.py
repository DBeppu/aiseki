# coding: UTF-8
import requests
from bs4 import BeautifulSoup
import re
import json
import datetime
import os
import boto3

def fetch_soup(url):
    r = requests.get(url) 
    return BeautifulSoup(r.text, "lxml")


def put_s3(data):
    s3 = boto3.client('s3',
                  aws_access_key_id='AKIAJJQBPHMOQQORWA4Q',
                  aws_secret_access_key='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',
                  region_name='ap-northeast-1')
    bucket_name = "reservele-aiseki"
    json_key = "assets/json/visitor.json"
    s3.put_object(ACL='public-read', Bucket=bucket_name, Key=json_key, Body = bytearray(json.dumps(data),'utf8'))


def crawlBJis():
    url = 'http://www.b-jis.com/system.html'
    targets = {
        "1":"fukuoka",
        # "2":"sapporo",
        # "3":"sapporo_b1",
        # "4":"sapporo_station",
        # "5":"namba",
        # "6":"kumamoto",
        # "7":"matsuyama"
    }
    res = []
    soup = fetch_soup(url)
    for script in soup.find_all('script', src=False):
        m = re.search('{"fukuoka\"\:.+}', script.get_text())
        if m == None:
            continue
        j_dict = json.loads(m.group())
        for k, v in targets.items():
            res.append({"aiseki_id":int(k),"men":j_dict[v]['shared']['mens_customer_num'], "women":j_dict[v]['shared']['ladys_customer_num'],"type":"people"})
        
    return res


def crawlOrientalLounge():
    url = 'http://www.oriental-lounge.com'
    soup = fetch_soup(url)
    targets = {
        # "8":'#box_sendai',#:'オリエンタル仙台',
        # "9":'#box_shinjuku',#:'オリエンタル新宿',
        # "10":'#box_shibuya',#:'オリエンタル渋谷',
        # "11":'#box_machida',#:'オリエンタル町田',
        # "12":'#box_nagoya',#:'オリエンタル名古屋',
        # "13":'#box_kyoto',#:'オリエンタル京都',
        # "14":'#box_shinsaibashi',#:'オリエンタル心斎橋',
        # "15":'#box_kobe',#:'オリエンタル神戸',
        # "16":'#box_hiroshima',#:'オリエンタル広島',
        "4":'#box_fukuoka',#:'オリエンタル福岡',
        # "18":'#box_kumamoto',#:'オリエンタル熊本',
        # "19":'#box_okinawa'#:'オリエンタル沖縄'
    }
    res = []
    for k,v in targets.items():
        dom = soup.select(v)
        if dom == None:
            continue        
        nums = dom[0].get_text().split('\xa0\xa0')
        res.append({"aiseki_id":int(k),"men":nums[0],"women":nums[1],"type":"people"})
        
    return res

def crawlEdgeBar():
    url = 'http://www.edge-bar.com/'
    soup = fetch_soup(url)
    targets = {
        "5":['#situation_left',1,'#man_left','#woman_left'],#:'相席ラウンジ＆バー エッジ ノアール(edge noir) 天神西通り店',
        "6":['#situation_left',0,'#man_left','#woman_left'],#:'相席ラウンジ&バー エッジ(edge)天神西通り店',
        "9":['#situation_right',0,'#man_right','#woman_right']#:相席ラウンジ＆バー エッジ(edge)大名店
    }
    res = []
    for k,v in targets.items():
        dom = soup.select(v[0])
        if dom == None:
            continue        
        men = dom[v[1]].select(v[2])[0].get_text()
        women = dom[v[1]].select(v[2])[0].get_text()
        res.append({"aiseki_id":int(k),"men":men.strip(),"women":women.strip(),"type":"%"})
        
    return res


def crawlLecirc():
    url = 'http://lecirc.com/index.php'
    soup = fetch_soup(url)
    targets = {
        "8":['#customer table tr:nth-of-type(1) td','#customer table tr:nth-of-type(2) td']#:相席ラウンジ ルサーク 大名店(Le Circ)
    }
    res = []
    for k,v in targets.items():
        men = 0
        if(soup.select(v[0])):
            men = soup.select(v[0])[0].get_text()
        if(soup.select(v[1])):
            women = soup.select(v[1])[0].get_text()
        res.append({"aiseki_id":int(k),"men":men.strip('äºº'),"women":women.strip('äºº'),"type":"people"})

    return res



visitor = crawlBJis()
visitor.extend(crawlOrientalLounge())
visitor.extend(crawlEdgeBar())
visitor.extend(crawlLecirc())
put_s3(visitor)
