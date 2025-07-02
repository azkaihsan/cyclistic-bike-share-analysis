# create a column called ride_length. Calculate the length of each ride by subtracting the column started_at from the column ended_at and format as HH:MM:SS (e.g 37:30:55). 
# Create a column called day_of_week, and calculate the day of the week that each ride started in each file. Format as General or as a number with no decimals, noting that 1 = Sunday and 7 = Saturday.
# Do this for each file.
# Here is the data row in dataset
# "ride_id","rideable_type","started_at","ended_at","start_station_name","start_station_id","end_station_name","end_station_id","start_lat","start_lng","end_lat","end_lng","member_casual"

import pandas as pd
import os
from datetime import timedelta

# Get all CSV files in the current directory
csv_files = [f for f in os.listdir('.') if f.endswith('.csv')]

for file in csv_files:
    print(f'Processing {file}...')
    df = pd.read_csv(file)
    # Ensure datetime columns are parsed
    df['started_at'] = pd.to_datetime(df['started_at'])
    df['ended_at'] = pd.to_datetime(df['ended_at'])
    # Calculate ride_length as timedelta
    df['ride_length'] = df['ended_at'] - df['started_at']
    # Format ride_length as HH:MM:SS
    df['ride_length'] = df['ride_length'].apply(lambda x: str(timedelta(seconds=int(x.total_seconds()))))
    # Calculate day_of_week (1=Sunday, 7=Saturday)
    df['day_of_week'] = df['started_at'].dt.dayofweek.apply(lambda x: (x + 1) % 7 + 1)
    # Save to new file
    output_file = file.replace('.csv', '_processed.csv')
    df.to_csv(output_file, index=False)
    print(f'Saved processed file as {output_file}')


