# Here is the data row in dataset
# "ride_id","rideable_type","started_at","ended_at","start_station_name","start_station_id","end_station_name","end_station_id","start_lat","start_lng","end_lat","end_lng","member_casual","ride_length","day_of_week"

# Create a visualization for :
# Bar Chart – Ride count by day of week by user type
# Line Chart – Monthly ride count trends by user type
# Box Plot / Histogram – Ride duration distribution
# Heatmap – Ride frequency by hour of day vs day of week
# Bar Chart – Top Start Stations by User Type
# Stacked Bar Chart – Bike Type Preference by User Type
# Grouped Bar Chart – Weekend vs. Weekday Ride Count by User Type
# Line Chart – Average Ride Duration Over Time (by Month)
# Bubble Chart – Hourly Ride Duration vs Frequency
# Save the visualization as a png file

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import calendar

# Helper to convert 'ride_length' to seconds
def hms_to_seconds(hms):
    try:
        if 'day' in str(hms):
            days_part, time_part = str(hms).split(', ')
            days = int(days_part.split()[0])
            h, m, s = map(int, time_part.split(':'))
            return days * 86400 + h * 3600 + m * 60 + s
        else:
            h, m, s = map(int, str(hms).split(':'))
            return h * 3600 + m * 60 + s
    except Exception:
        return None

# Helper to convert YYYYMM to 'Month YYYY'
def format_month(ym):
    ym = str(ym)
    year = int(ym[:4])
    month = int(ym[4:])
    return f"{calendar.month_name[month]} {year}"

# Load all cleaned monthly files (sample 100,000 rows per file for memory)
csv_files = [f for f in os.listdir('.') if f.endswith('_cleaned.csv')]
frames = []
for file in csv_files:
    df = pd.read_csv(file, nrows=100000)
    df['month'] = file[:6]
    frames.append(df)
df = pd.concat(frames, ignore_index=True)

# Preprocessing
df['ride_length_sec'] = df['ride_length'].apply(hms_to_seconds)
df['started_at'] = pd.to_datetime(df['started_at'], errors='coerce')
df['hour_of_day'] = df['started_at'].dt.hour
df['day_of_week'] = df['day_of_week'].astype(int)
df['is_weekend'] = df['day_of_week'].apply(lambda x: x == 1 or x == 7)

# After loading and concatenating dataframes:
df['month_label'] = df['month'].apply(format_month)

# 1. Bar Chart – Ride count by day of week by user type
plt.figure(figsize=(10,6))
sns.countplot(data=df, x='day_of_week', hue='member_casual', palette='Set2')
plt.title('Ride Count by Day of Week and User Type')
plt.xlabel('Day of Week (1=Sunday, 7=Saturday)')
plt.ylabel('Ride Count')
plt.legend(title='User Type')
plt.savefig('ride_count_by_dayofweek_usertype.png')
plt.close()

# 2. Line Chart – Monthly ride count trends by user type
plt.figure(figsize=(10,6))
monthly_counts = df.groupby(['month', 'month_label', 'member_casual'])['ride_id'].count().reset_index()
monthly_counts = monthly_counts.sort_values('month')
sns.lineplot(data=monthly_counts, x='month_label', y='ride_id', hue='member_casual', marker='o')
plt.title('Monthly Ride Count Trends by User Type')
plt.xlabel('Month')
plt.ylabel('Ride Count')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('monthly_ride_count_trends.png')
plt.close()

# 3. Box Plot – Ride duration distribution
plt.figure(figsize=(10,6))
sns.boxplot(data=df, x='member_casual', y='ride_length_sec', showfliers=False)
plt.title('Ride Duration Distribution by User Type')
plt.ylabel('Ride Duration (seconds)')
plt.savefig('ride_duration_boxplot.png')
plt.close()

# 4. Histogram – Ride duration distribution
plt.figure(figsize=(10,6))
sns.histplot(data=df, x='ride_length_sec', hue='member_casual', bins=50, kde=True, element='step')
plt.title('Ride Duration Histogram by User Type')
plt.xlabel('Ride Duration (seconds)')
plt.savefig('ride_duration_histogram.png')
plt.close()

# 5. Heatmap – Ride frequency by hour of day vs day of week
heatmap_data = df.groupby(['hour_of_day', 'day_of_week'])['ride_id'].count().unstack(fill_value=0)
plt.figure(figsize=(12,7))
sns.heatmap(heatmap_data, cmap='YlGnBu', annot=False)
plt.title('Ride Frequency by Hour of Day vs Day of Week')
plt.xlabel('Day of Week (1=Sunday, 7=Saturday)')
plt.ylabel('Hour of Day')
plt.savefig('ride_frequency_heatmap.png')
plt.close()

# 6. Bar Chart – Top Start Stations by User Type
top_stations = df.groupby(['member_casual', 'start_station_name'])['ride_id'].count().reset_index()
top_stations = top_stations.sort_values(['member_casual','ride_id'], ascending=[True,False]).groupby('member_casual').head(10)
plt.figure(figsize=(18,10))
sns.barplot(data=top_stations, y='start_station_name', x='ride_id', hue='member_casual')
plt.title('Top Start Stations by User Type')
plt.xlabel('Ride Count')
plt.ylabel('Start Station')
plt.tight_layout()
plt.savefig('top_start_stations.png')
plt.close()

# 7. Stacked Bar Chart – Bike Type Preference by User Type
bike_type = df.groupby(['member_casual', 'rideable_type'])['ride_id'].count().unstack(fill_value=0)
bike_type.plot(kind='bar', stacked=True, figsize=(10,7), colormap='tab20')
plt.title('Bike Type Preference by User Type')
plt.xlabel('User Type')
plt.ylabel('Ride Count')
plt.savefig('bike_type_preference.png')
plt.close()

# 8. Grouped Bar Chart – Weekend vs. Weekday Ride Count by User Type
weekpart = df.groupby(['member_casual', 'is_weekend'])['ride_id'].count().reset_index()
weekpart['weekpart'] = weekpart['is_weekend'].map({True:'Weekend', False:'Weekday'})
plt.figure(figsize=(8,6))
sns.barplot(data=weekpart, x='member_casual', y='ride_id', hue='weekpart')
plt.title('Weekend vs. Weekday Ride Count by User Type')
plt.xlabel('User Type')
plt.ylabel('Ride Count')
plt.savefig('weekend_vs_weekday_ridecount.png')
plt.close()

# 9. Line Chart – Average Ride Duration Over Time (by Month)
monthly_avg = df.groupby(['month', 'month_label', 'member_casual'])['ride_length_sec'].mean().reset_index()
monthly_avg = monthly_avg.sort_values('month')
plt.figure(figsize=(10,6))
sns.lineplot(data=monthly_avg, x='month_label', y='ride_length_sec', hue='member_casual', marker='o')
plt.title('Average Ride Duration Over Time by User Type')
plt.xlabel('Month')
plt.ylabel('Average Ride Duration (seconds)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('avg_ride_duration_over_time.png')
plt.close()

# 10. Bubble Chart – Hourly Ride Duration vs Frequency
bubble = df.groupby(['hour_of_day', 'member_casual']).agg({'ride_id':'count', 'ride_length_sec':'mean'}).reset_index()
plt.figure(figsize=(12,7))
sns.scatterplot(data=bubble, x='hour_of_day', y='ride_length_sec', size='ride_id', hue='member_casual', alpha=0.6, sizes=(20, 500))
plt.title('Hourly Ride Duration vs Frequency')
plt.xlabel('Hour of Day')
plt.ylabel('Average Ride Duration (seconds)')
plt.legend(title='User Type', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.savefig('hourly_ride_duration_vs_frequency.png', bbox_inches='tight')
plt.close()



