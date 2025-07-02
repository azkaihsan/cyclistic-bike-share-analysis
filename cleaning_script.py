import pandas as pd
import os
from datetime import timedelta

# Helper function to convert 'ride_length' string to seconds
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
        return None  # Handle malformed time strings

# Define thresholds
MIN_SECONDS = 60             # 1 minute
MAX_SECONDS = 86400          # 24 hours

# Process each processed file
csv_files = [f for f in os.listdir('.') if f.endswith('_processed.csv')]

for file in csv_files:
    print(f'\nChecking {file}...')
    df = pd.read_csv(file)

    # Convert ride_length to seconds
    df['ride_length_sec'] = df['ride_length'].apply(hms_to_seconds)

    # Identify missing values
    missing_summary = df.isnull().sum()
    print("\nMissing values per column:")
    print(missing_summary[missing_summary > 0])

    # Flag outliers
    outliers = df[(df['ride_length_sec'] < MIN_SECONDS) | (df['ride_length_sec'] > MAX_SECONDS)]
    print(f"\nOutlier rides (<1 min or >24 hrs): {len(outliers)}")

    # Optionally, remove outliers
    cleaned_df = df[(df['ride_length_sec'] >= MIN_SECONDS) & (df['ride_length_sec'] <= MAX_SECONDS)]

    # Save cleaned file
    output_file = file.replace('_processed.csv', '_cleaned.csv')
    cleaned_df.to_csv(output_file, index=False)
    print(f"Cleaned data saved as {output_file} ({len(cleaned_df)} rows)")
