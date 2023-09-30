import pandas as pd
import time
import random

# Sample data for updating parameters (except locations)
def generate_random_data():
    status_options = ['MODERATE', 'GOOD', 'POOR']
    aqi_in = random.randint(20, 110)
    pm25 = random.randint(0, 60)
    pm10 = random.randint(20, 110)
    temp = random.uniform(28, 31)
    humid = random.randint(60, 70)
    return random.choice(status_options), aqi_in, pm25, pm10, temp, humid

# Define the initial dataset with all locations
data = {
    'Locations': [
        'ARK Serene County', 'Bapuji Nagar', 'BETHANY SCH', 'BLR 103', 'BLR 76',
        'Bommanhalli', 'Brigade Road', 'Brookefield', 'Btm', 'BTM Layout',
        'Bwssb Kadabesanahalli', 'Chansandra', 'Chinnapanhalli', 'City Railway Station',
        'Cox Town', 'CV Raman Nagar', 'Devasthanagalu', 'Doddanekundi', 'Ejipura',
        'Harlur', 'Hebbal', 'Hombegowda Nagar', 'Indian Institute of Mgmt', 'ISRO Colony',
        'Jayanagar 5Th Block', 'Kalyan Nagar', 'Koramangala', 'Krishnarajapura',
        'Kundalahalli Colony', 'Maruthi Nagar', 'Mathikare', 'Nagashetty Hall',
        'Neeladri Nagar', 'NR Colony MH', 'Peenya', 'PES University', 'Prestige Park View',
        'Saneguravahalli', 'Sanjaynagar', 'Siddapura', 'Silk Board', 'SIPCOT Phase 1',
        'SJRI 34', 'Tavarekere', 'Venkatachary Nagar', 'Vijay Nagar', 'Whitefield'
    ],
    'Status': ['MODERATE'] * 50,
    'AQI-IN': [29] * 50,
    'PM2.5': [16] * 50,
    'PM10': [29] * 50,
    'Temp': [31] * 50,
    'Humid': [62] * 50
}

df = pd.DataFrame(data)

while True:
    # Update parameters (except Locations) with new data
    for i in range(len(df)):
        status, aqi_in, pm25, pm10, temp, humid = generate_random_data()
        df.at[i, 'Status'] = status
        df.at[i, 'AQI-IN'] = aqi_in
        df.at[i, 'PM2.5'] = pm25
        df.at[i, 'PM10'] = pm10
        df.at[i, 'Temp'] = temp
        df.at[i, 'Humid'] = humid
    
    # Display the updated DataFrame
    print(df)
    
    # Wait for 5 minutes before the next update
    time.sleep(300)  # 5 minutes in seconds
