# Here is the data row in dataset
# "ride_id","rideable_type","started_at","ended_at","start_station_name","start_station_id","end_station_name","end_station_id","start_lat","start_lng","end_lat","end_lng","member_casual","ride_length","day_of_week"

# For each file, calculate the following:
# 1. Mean of ride_length 
# 2. Max of ride_length
# 3. Mode of day_of_week

# For each file, calculate the following:
# 1. The average ride length for members and casual riders
# 2. The average ride length for users by day of the week
# 3. The number of rides for users by day of the week

import pandas as pd
import os
from datetime import timedelta
import calendar

# Helper to convert 'ride_length' to seconds
def hms_to_seconds(hms):
    try:
        if 'day' in hms:
            days_part, time_part = hms.split(', ')
            days = int(days_part.split()[0])
            h, m, s = map(int, time_part.split(':'))
            return days * 86400 + h * 3600 + m * 60 + s
        else:
            h, m, s = map(int, hms.split(':'))
            return h * 3600 + m * 60 + s
    except Exception:
        return None

# Load all cleaned monthly files
csv_files = [f for f in os.listdir('.') if f.endswith('_cleaned.csv')]

for file in csv_files:
    print(f"\nAnalyzing {file}...")
    df = pd.read_csv(file)

    # Convert ride_length to seconds
    df['ride_length_sec'] = df['ride_length'].apply(hms_to_seconds)

    # Convert started_at to datetime and extract hour
    df['started_at'] = pd.to_datetime(df['started_at'], errors='coerce')
    df['hour_of_day'] = df['started_at'].dt.hour

    # Weekend or Weekday column
    df['is_weekend'] = df['day_of_week'].apply(lambda x: x == 1 or x == 7)

    # ========================
    # Core Statistics
    # ========================
    mean_ride_length = timedelta(seconds=int(df['ride_length_sec'].mean()))
    max_ride_length = timedelta(seconds=int(df['ride_length_sec'].max()))
    mode_day_of_week = df['day_of_week'].mode()[0]

    print(f"Mean ride length: {mean_ride_length}")
    print(f"Max ride length: {max_ride_length}")
    print(f"Mode of day_of_week: {mode_day_of_week} ({calendar.day_name[mode_day_of_week - 1]})")

    # ========================
    # Ride Length by User Type
    # ========================
    avg_by_type = df.groupby('member_casual')['ride_length_sec'].mean().apply(lambda x: str(timedelta(seconds=int(x))))
    print("\nAverage ride length by user type:")
    print(avg_by_type)

    # ========================
    # Ride Length by Day of Week
    # ========================
    avg_by_day = df.groupby(['member_casual', 'day_of_week'])['ride_length_sec'].mean().apply(lambda x: str(timedelta(seconds=int(x))))
    print("\nAverage ride length by user type and day of week:")
    print(avg_by_day)

    count_by_day = df.groupby(['member_casual', 'day_of_week'])['ride_id'].count()
    print("\nNumber of rides by user type and day of week:")
    print(count_by_day)

    # ========================
    # Ride Count by Hour of Day
    # ========================
    rides_by_hour = df.groupby(['member_casual', 'hour_of_day'])['ride_id'].count()
    print("\nRide count by hour of day:")
    print(rides_by_hour)

    # ========================
    # Ride Type Preferences
    # ========================
    ride_count_by_type = df.groupby(['member_casual', 'rideable_type'])['ride_id'].count()
    avg_duration_by_type = df.groupby(['member_casual', 'rideable_type'])['ride_length_sec'].mean().apply(lambda x: str(timedelta(seconds=int(x))))
    print("\nRide count by bike type:")
    print(ride_count_by_type)
    print("\nAverage ride duration by bike type:")
    print(avg_duration_by_type)

    # ========================
    # Weekend vs Weekday Comparison
    # ========================
    ride_count_weekpart = df.groupby(['member_casual', 'is_weekend'])['ride_id'].count()
    avg_duration_weekpart = df.groupby(['member_casual', 'is_weekend'])['ride_length_sec'].mean().apply(lambda x: str(timedelta(seconds=int(x))))
    print("\nRide count: Weekend vs Weekday")
    print(ride_count_weekpart)
    print("\nAverage duration: Weekend vs Weekday")
    print(avg_duration_weekpart)

    # ========================
    # Monthly Ride Count (Optional: parse from file name)
    # ========================
    month_label = file[:6]  # '202406', etc.
    ride_count_month = df.groupby('member_casual')['ride_id'].count()
    print(f"\nRide count in {month_label}:")
    print(ride_count_month)
