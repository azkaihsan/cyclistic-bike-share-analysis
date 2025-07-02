import pandas as pd
import os
from datetime import timedelta

# Helper to convert ride_length (HH:MM:SS) to total seconds
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

# Step 1: Merge all _cleaned.csv files into one full-year DataFrame
all_files = [f for f in os.listdir('.') if f.endswith('_cleaned.csv')]
merged_df = pd.DataFrame()

for file in all_files:
    df = pd.read_csv(file)
    df['source_file'] = file
    merged_df = pd.concat([merged_df, df], ignore_index=True)

# Step 2: Prepare data
merged_df['ride_length_sec'] = merged_df['ride_length'].apply(hms_to_seconds)
merged_df['started_at'] = pd.to_datetime(merged_df['started_at'], errors='coerce')
merged_df['day_of_week'] = merged_df['started_at'].dt.weekday.apply(lambda x: (x + 1) % 7 + 1)
merged_df['is_weekend'] = merged_df['day_of_week'].apply(lambda x: x == 1 or x == 7)
merged_df['hour_of_day'] = merged_df['started_at'].dt.hour

# Step 3: Compute full-year summary per user type
summary = []

for user_type in merged_df['member_casual'].unique():
    sub = merged_df[merged_df['member_casual'] == user_type]
    summary.append({
        'User_Type': user_type,
        'Total_Rides': len(sub),
        'Mean_Ride_Length_sec': round(sub['ride_length_sec'].mean(), 2),
        'Max_Ride_Length_sec': sub['ride_length_sec'].max(),
        'Mode_Day_of_Week': sub['day_of_week'].mode()[0] if not sub['day_of_week'].isnull().all() else None,
        'Total_Weekend_Rides': len(sub[sub['is_weekend']]),
        'Total_Weekday_Rides': len(sub[~sub['is_weekend']]),
        'Avg_Weekend_Ride_Length_sec': round(sub[sub['is_weekend']]['ride_length_sec'].mean(), 2),
        'Avg_Weekday_Ride_Length_sec': round(sub[~sub['is_weekend']]['ride_length_sec'].mean(), 2)
    })

# Step 4: Save results
summary_df = pd.DataFrame(summary)
merged_df.to_csv('cyclistic_full_year_data.csv', index=False)
summary_df.to_csv('cyclistic_full_year_summary.csv', index=False)

print("Full-year data saved as 'cyclistic_full_year_data.csv'")
print("Full-year summary saved as 'cyclistic_full_year_summary.csv'")
