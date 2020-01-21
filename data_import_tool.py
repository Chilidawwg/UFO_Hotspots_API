from sqlalchemy import create_engine

import pandas as pd

# read CSV file
column_names = ['date_time', 'shape', 'duration', 'city', 'state', 'latitude', 'longitude', 'comments']

df = pd.read_csv('sightings_data.csv', header=None, names=column_names)
print(df)

df = pd.read_csv('sightings_data.csv', header=0)
print(df)

# get authenticated by database and import csv.

engine = create_engine('mysql://root:root@127.0.0.1/sightings', pool_pre_ping=True)
with engine.connect() as conn, conn.begin():
    df.to_sql('ufo_api_sighting', conn, if_exists='append', index=False)
