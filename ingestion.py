import os
import pandas as pd
from sqlalchemy import create_engine
import click

@click.command()
@click.option('--user')
@click.option('--password')
@click.option('--host')
@click.option('--port')
@click.option('--db')
@click.option('--table_name')
@click.option('--url')
def main(user, password, host, port, db, table_name, url):
    file_name = 'data.parquet' if 'parquet' in url else 'data.csv'
    
    print(f"Downloading {url}...")
    
    os.system(f"curl -L {url} -o {file_name}")

    engine = create_engine(f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}')

    if file_name.endswith('.parquet'):
        df = pd.read_parquet(file_name)
    else:
        df = pd.read_csv(file_name, low_memory=False)

    
    for col in ['lpep_pickup_datetime', 'lpep_dropoff_datetime']:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col])

    print(f"Ingesting {len(df)} rows...")
    df.to_sql(name=table_name, con=engine, if_exists='replace', index=False)
    print("Success!")

if __name__ == '__main__':
    main()