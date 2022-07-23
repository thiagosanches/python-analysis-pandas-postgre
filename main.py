#!/usr/bin/python3

import pandas as pd
import csv

df = pd.read_csv("filtered-data.csv", parse_dates=[["date", "time"]])
dfByDateTime = df.groupby('request_ip').resample('300S', on="date_time").request_ip.count()

dfByDateTimeOrdered = dfByDateTime.sort_values('date_time', ascending=False)
dfByDateTimeOrdered.to_csv('resampled-data.csv')
