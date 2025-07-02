import pandas as pd
import os
from datetime import timedelta
import calendar

# Helper to convert 'ride_length' to total seconds
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
    except:
        return None

# Summary table will be stored here
summary_records = []

# List of all cleaned monthly files
csv_files = [f for f in os.listdir('.') if f.endswith('_cleaned.csv')]

for file in csv_files:
    print(f"Analyzing {file}...")
    df = pd.read_csv(file)

    # Convert columns
    df['ride_length_sec'] = df['ride_length'].apply(hms_to_seconds)
    df['started_at'] = pd.to_datetime(df['started_at'], errors='coerce')
    df['hour_of_day'] = df['started_at'].dt.hour
    df['is_weekend'] = df['day_of_week'].apply(lambda x: x == 1 or x == 7)
    df['month'] = file[:6]

    # Analyze by user type
    for user_type in df['member_casual'].unique():
        sub = df[df['member_casual'] == user_type]
        record = {
            'Month': file[:6],
            'User_Type': user_type,
            'Ride_Count': len(sub),
            'Mean_Ride_Length_sec': round(sub['ride_length_sec'].mean(), 2),
            'Max_Ride_Length_sec': sub['ride_length_sec'].max(),
            'Mode_Day_of_Week': sub['day_of_week'].mode()[0] if not sub['day_of_week'].isnull().all() else None,
            'Weekend_Rides': len(sub[sub['is_weekend'] == True]),
            'Weekday_Rides': len(sub[sub['is_weekend'] == False]),
            'Avg_Weekend_Ride_Length_sec': round(sub[sub['is_weekend']]['ride_length_sec'].mean(), 2),
            'Avg_Weekday_Ride_Length_sec': round(sub[~sub['is_weekend']]['ride_length_sec'].mean(), 2)
        }
        summary_records.append(record)

# Save the summary to a CSV file
summary_df = pd.DataFrame(summary_records)
summary_df.to_csv("cyclistic_monthly_summary.csv", index=False)

print("✅ Summary saved to 'cyclistic_monthly_summary.csv'")
