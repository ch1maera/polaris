import pandas as pd
import time
import requests


## ESI url segments used to fetch data
ESI_BASE = 'https://esi.tech.ccp.is/latest/markets/'
ESI_SOURCE = '/history/?datasource=tranquility&type_id='

## Regions in EVE that have NPC corps that accept blue loot buy orders
region_ids = ('10000054','10000001','10000036','10000043','10000064','10000037',
      '10000067','10000011','10000030','10000052','10000065','10000016',
      '10000042','10000028','10000041','10000020','10000033','10000002')

## Type IDs for the four blue loot items, and their respective NPC values
type_ids = ('30746','30744','30745','30747')
buy_order_price = (1500000,200000,500000,5000000)

new_list = []

PATH = 'new_eden_sleeper_loot_' + time.strftime('%d-%m-%Y') + '.csv'

def main():
    for type_id in type_ids:
        for region_id in region_ids:
            url = url_build(region_id,type_id)

            req = requests.get(url)
            req.raise_for_status()
            data = req.json()

            add_region_id(region_id,data)
            add_value(buy_order_price[type_ids.index(type_id)],data)

            new_list.extend(data)

    df = format_df(new_list)

    df.to_csv(PATH)

def add_region_id(regionID,a_list):
    for i in range(len(a_list)):
        a_list[i]['regionid'] = regionID
    return a_list

def add_value(value,a_list):
    for i in range(len(a_list)):
        a_list[i]['value'] = value * a_list[i]['volume']
    return a_list

def format_df(a_list):
    df = pd.DataFrame(a_list)
    df_grouped = df.groupby('date')
    df_agg = df_grouped.agg({'value' : 'sum'})
    df_agg['rolling_average-14'] = df_agg['value'].rolling(14).mean()
    return df_agg

def url_build(region_id,type_id):
    url = ESI_BASE + region_id + ESI_SOURCE + type_id
    return url

if __name__ == "__main__": main()