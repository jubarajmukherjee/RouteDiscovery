import pandas as pd
import time
import random
import numpy as np
from sklearn.cluster import KMeans
km = KMeans(n_clusters=3,n_init='auto')

# Sample data for updating parameters (except locations)
def generate_random_data():
    
    aqi_in = random.randint(20, 110)
    pm25 = random.randint(0, 60)
    pm10 = random.randint(20, 110)
    temp = random.uniform(28, 31)
    humid = random.randint(60, 70)
    return aqi_in, pm25, pm10, temp, humid

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
    'AQI-IN': [29] * 49,
    'PM2.5': [16] * 49,
    'PM10': [29] * 49,
    'Temp': [31] * 49,
    'Humid': [62] * 49
}

df = pd.DataFrame(data)

while True:
    # Update parameters (except Locations) with new data
    for i in range(len(df)):
        aqi_in, pm25, pm10, temp, humid = generate_random_data()
        df.at[i, 'AQI-IN'] = aqi_in
        df.at[i, 'PM2.5'] = pm25
        df.at[i, 'PM10'] = pm10
        df.at[i, 'Temp'] = temp
        df.at[i, 'Humid'] = humid
    
    # Display the updated DataFrame
    
    pred = km.fit_predict(df[['AQI-IN','PM2.5','PM10','Temp','Humid']])
    df2 = pd.DataFrame(km.cluster_centers_,columns=['AQI','PM1','PM2','TEMP','HUMID'])
    w1 = 0.6
    w2 = 0.15
    w3 = 0.15
    w4=  0.05
    w5 = 0.05
    s0 = np.mean(df2.iloc[0][0]*w1+df2.iloc[0][1]*w2+df2.iloc[0][2]*w3+df2.iloc[0][3]*w4+df2.iloc[0][4]*w5/(w1+w2+w3+w4+w5))
    s1 = np.mean(df2.iloc[1][0]*w1+df2.iloc[1][1]*w2+df2.iloc[1][2]*w3+df2.iloc[1][3]*w4+df2.iloc[1][4]*w5/(w1+w2+w3+w4+w5))
    s2 = np.mean(df2.iloc[2][0]*w1+df2.iloc[2][1]*w2+df2.iloc[2][2]*w3+df2.iloc[2][3]*w4+df2.iloc[2][4]*w5/(w1+w2+w3+w4+w5))
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