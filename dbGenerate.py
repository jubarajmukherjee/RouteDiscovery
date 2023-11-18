import pandas as pd
import time
import random
import numpy as np
import urllib.request as urllib2
import json
from sklearn.cluster import KMeans
km = KMeans(n_clusters=3,n_init='auto')
READ_API_KEY='RSM668VKEAVTD39O'
CHANNEL_ID= '2329603'

def read_koramangala2():
    TS = urllib2.urlopen("http://api.thingspeak.com/channels/%s/feeds/last.json?api_key=%s" \
                       % (CHANNEL_ID,READ_API_KEY))

    response = TS.read()
    data2=json.loads(response)   
    TS.close()
    data2 = pd.DataFrame({'temp':[data2['field1']],'humid':[data2['field2']],'AQI':[data2['field6']],'Dust':[data2['field7']]})
    
    return data2

def read_koramangala():
    TS = urllib2.urlopen("http://api.thingspeak.com/channels/%s/feeds/?api_key=%s" 
                       % (CHANNEL_ID,READ_API_KEY))

    response = TS.read()
    data2=json.loads(response)   
    TS.close()
    data2=data2['feeds']
    data2= pd.DataFrame(data2)
    data2 = data2.drop(['created_at','entry_id','field3','field4','field5'],axis=1)
    data2.columns = ['temp','humid','AQI','Dust']
    return data2

# Sample data for updating parameters (except locations)
def generate_random_data():
    data2 = read_koramangala()
    AQI = random.uniform(float(np.min(data2['AQI'])),float(np.max(data2['AQI'])))
    Dust = random.uniform(float(np.min(data2['Dust'])), float(np.max(data2['Dust'])))
    temp = random.uniform(float(np.min(data2['temp'])), float(np.max(data2['temp'])))
    humid = random.uniform(float(np.min(data2['humid'])),float(np.max(data2['humid'])))
    return AQI, Dust, temp, humid

# Define the initial dataset with all locations
data = {
    'Locations': [
        'ARK Serene County', 
        'Bapuji Nagar', 
        'BETHANY SCH', 
        'BLR 103', 
        'BLR 76',
        'Bommanhalli', 
        'Brigade Road', 
        'Brookefield', 
        'Btm', 
        'BTM Layout',
        'Bwssb Kadabesanahalli',
          'Chansandra', 
          'Chinnapanhalli',
            'City Railway Station',
        'Cox Town', 
        'CV Raman Nagar', 
        'Devasthanagalu',
          'Doddanekundi',
            'Ejipura',
        'Harlur',
          'Hebbal', 
          'Hombegowda Nagar', 
          'Indian Institute of Mgmt',
            'ISRO Colony',
        'Jayanagar 5Th Block', 
        'Kalyan Nagar', 
        'Koramangala', 
        'Krishnarajapura',
        'Kundalahalli Colony', 
        'Maruthi Nagar', 
        'Mathikare', 
        'Nagashetty Hall',
        'Neeladri Nagar', 
        'NR Colony MH', 
        'Peenya', 
        'PES University', 
        'Prestige Park View',
        'Saneguravahalli',
          'Sanjaynagar', 
          'Siddapura', 
          'Silk Board', 
          'SIPCOT Phase 1',
        'SJRI 34', 
        'Tavarekere', 
        'Venkatachary Nagar',
          'Vijay Nagar', 
          'Whitefield',
          'Domlur',
          'HSR Layout'
    ],
    'AQI': [29.0] * 49,
    'Dust': [16.0] * 49,
    'temp': [31.0] * 49,
    'humid': [62.0] * 49
}

df = pd.DataFrame(data)

while True:
    # Update parameters (except Locations) with new data
    
    for i in range(len(df)):
        if df.at[i,'Locations'] == 'Koramangala':
            data3 = read_koramangala2()
            df.at[i, 'AQI'] = float(data3.iloc[0]['AQI'])
            df.at[i, 'Dust'] = float(data3.iloc[0]['Dust'])
            df.at[i, 'temp'] = float(data3.iloc[0]['temp'])
            df.at[i, 'humid'] = float(data3.iloc[0]['humid'])

        else:
            AQI, Dust, temp, humid = generate_random_data()
            df.at[i, 'AQI'] = AQI
            df.at[i, 'Dust'] = Dust
            df.at[i, 'temp'] = temp
            df.at[i, 'humid'] = humid
    
    # Display the updated DataFrame
    
    pred = km.fit_predict(df[['AQI','Dust','temp','humid']])
    df2 = pd.DataFrame(km.cluster_centers_,columns=['AQI','Dust','temp','humid'])
    w1 = 0.6
    w2 = 0.3
    w4=  0.05
    w5 = 0.05
    s0 = np.mean(df2.iloc[0][0]*w1+df2.iloc[0][1]*w2+df2.iloc[0][2]*w4+df2.iloc[0][3]*w5/(w1+w2+w4+w5))
    s1 = np.mean(df2.iloc[1][0]*w1+df2.iloc[1][1]*w2+df2.iloc[1][2]*w4+df2.iloc[1][3]*w5/(w1+w2+w4+w5))
    s2 = np.mean(df2.iloc[2][0]*w1+df2.iloc[2][1]*w2+df2.iloc[2][2]*w4+df2.iloc[2][3]*w5/(w1+w2+w4+w5))
    L = [s0,s1,s2]
    L.sort()
    print(L)
    print(s0,s1,s2)
    if L[0] == s0:
        l0 = 'GOOD'
        l0_score=1
    elif L[0] == s1:
        l1 = 'GOOD'
        l1_score=1
    else:
        l2 = 'GOOD'
        l2_score=1
    if L[1] == s0:
        l0 = 'MODERATE'
        l0_score=2
    elif L[1] == s1:
        l1 = 'MODERATE'
        l1_score=2
    else:
        l2 = 'MODERATE'
        l2_score=2

    if L[2] == s0:
        l0 = 'BAD'
        l0_score=3
    elif L[2] == s1:
        l1 = 'BAD'
        l1_score=3
    else:
        l2 = 'BAD'
        l2_score=3
    df['label'] = pred
    df['score'] = pred
    df['label'] = df['label'].map({0:l0,1:l1,2:l2})
    df['score'] = df['score'].map({0:l0_score,1:l1_score,2:l2_score})
    df.to_csv('file1.csv')
    print(df)
    # Wait for 5 minutes before the next update
    break  # 5 minutes in seconds