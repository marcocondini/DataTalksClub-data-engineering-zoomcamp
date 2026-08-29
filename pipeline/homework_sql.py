#!/usr/bin/env python
# coding: utf-8

# In[2]:

from sqlalchemy import create_engine
import pandas as pd
import click
from tqdm.auto import tqdm
@click.command()
@click.option('--pg-user', default='root', help='PostgreSQL user')
@click.option('--pg-pass', default='root', help='PostgreSQL password')
@click.option('--pg-host', default='localhost', help='PostgreSQL host')
@click.option('--pg-port', default=5432, type=int, help='PostgreSQL port')
@click.option('--pg-db', default='ny_taxi', help='PostgreSQL database name')
@click.option('--chunksize', default=100000, type=int, help='Chunk size for data ingestion')
def run(pg_user, pg_pass, pg_host, pg_port, pg_db, chunksize):
    engine = create_engine(f'postgresql+psycopg://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')

    df_green_taxi = pd.read_parquet(
            "https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-11.parquet",
        )
    df_taxi_zone = pd.read_csv(
            "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv"
        )
    df_dict = {
        "df_green_taxi_table": df_green_taxi,
        "df_taxi_zone_table": df_taxi_zone
    }
    for table_name, df in df_dict.items():
        # Insert chunk
        df.to_sql(
            name=table_name,
            con=engine,
            if_exists="replace"
        )

        print("Inserted:", len(df))



'''
#sql file
#Q3
select count(1) from 
df_green_taxi_table t_green
where CAST(t_green."lpep_pickup_datetime" AS DATE) >= '2025-11-01'
and CAST(t_green."lpep_pickup_datetime" AS DATE) < '2025-12-01'
and t_green."trip_distance" <= 1

#Q4
select 
lpep_pickup_datetime,
trip_distance AS "distance"
from 
df_green_taxi_table t_green
where t_green."trip_distance" <100
ORDER BY
"distance" DESC

Q5
select 
    tip_amount,
    zoD."Zone" AS "dropoff_loc",
    zoU."Zone" AS "pickup_loc"
from 
df_green_taxi_table as t
JOIN
df_taxi_zone_table as zoD
ON t."DOLocationID" = zoD."LocationID"
JOIN
df_taxi_zone_table as zoU
ON t."PULocationID" = zoU."LocationID"
Where zoU."Zone" =  'East Harlem North'
Order BY tip_amount DESC
'''

if __name__ == "__main__":
    run()



