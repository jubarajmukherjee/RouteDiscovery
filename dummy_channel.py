import requests
import time
import urllib.request as urllib2
import json
import random

READ_API_KEY='RSM668VKEAVTD39O'
CHANNEL_ID= '2329603'
import pandas as pd 
def read_koramangala():
    TS = urllib2.urlopen("http://api.thingspeak.com/channels/%s/feeds/?api_key=%s" 
                       % (CHANNEL_ID,READ_API_KEY))

    response = TS.read()
    data2=json.loads(response)   
    TS.close()
    data2=data2['feeds']
    data2= pd.DataFrame(data2)
    data2 = data2.drop(['created_at','entry_id'],axis=1)
    
    return data2

while 1:
    df = read_koramangala()
    field1 = random.uniform(float(min(df['field1'])),float(max(df['field1'])))
    field2 = random.uniform(float(min(df['field2'])),float(max(df['field2'])))
    field3 = random.uniform(float(min(df['field3'])),float(max(df['field3'])))
    field4 = random.uniform(float(min(df['field4'])),float(max(df['field4'])))
    field5 = random.uniform(float(min(df['field5'])),float(max(df['field5'])))
    field7= random.uniform(float(min(df['field7'])),float(max(df['field7'])))
    field6 = random.uniform(float(min(df['field6'])),float(max(df['field6'])))
    URL =  f'https://api.thingspeak.com/update?api_key=QLEQE2R023AWUDM0&field1={field1}&field2={field2}&field3={field3}&field4={field4}&field5={field5}&field6={field6}&field7={field7}'
    response = requests.get(URL)
    print(response)
    time.sleep(15)
    
