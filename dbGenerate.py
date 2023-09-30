import pandas as pd
import time
import random

# Sample data for updating parameters (except locations)
update_data = {
    'Status': ['MODERATE', 'GOOD', 'POOR', 'POOR', 'MODERATE'],
    'AQI-IN': [random.randint(20, 110) for _ in range(5)],
    'PM2.5': [random.randint(0, 60) for _ in range(5)],
    'PM10': [random.randint(20, 110) for _ in range(5)],
    'Temp': [random.uniform(28, 31) for _ in range(5)],
    'Humid': [random.randint(60, 70) for _ in range(5)],
}

# Load the existing dataset
data = {
    'Locations': [
        'ARK Serene County', 'Bapuji Nagar', 'BETHANY SCH', 'BLR 103', 'BLR 76'
    ],
    'Status': ['MODERATE', 'GOOD', 'POOR', 'POOR', 'MODERATE'],
    'AQI-IN': [29, 48, 92, 80, 80],
    'PM2.5': [16, 12, 55, 38, 39],
    'PM10': [29, 48, 88, 56, 57],
    'Temp': [31, 28, 31, 31, 28],
    'Humid': [62, 70, 60, 60, 60]
}

df = pd.DataFrame(data)

while True:
    # Update parameters (except Locations) with new data
    for i, location in enumerate(df['Locations']):
        for column in update_data:
            if column != 'Locations':
                df.at[i, column] = update_data[column][i]
    
    # Display the updated DataFrame
    print(df)
    
    # Wait for 5 minutes before the next update
    time.sleep(300)  # 5 minutes in seconds
