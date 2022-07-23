#!/usr/bin/python3
import pandas as pd
import csv

print("Going to read the CSV file...")
df = pd.read_csv("filtered-data.csv", parse_dates=[["date", "time"]])
print("Going to read the CSV file... [OK]")

print("Going to groupby and resample...")
dfByDateTime = df.groupby('request_ip').resample('300S', on="date_time").request_ip.count()
print("Going to groupby and resample... [OK]")

dfByDateTimeOrdered = dfByDateTime.sort_values('date_time', ascending=False)
dfByDateTimeOrdered.to_csv('resampled-data.csv')
