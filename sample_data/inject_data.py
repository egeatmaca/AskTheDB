import pandas as pd
import json
import os
from sqlalchemy import create_engine

def inject_data():
    # Create engine
    host = os.environ.get('POSTGRES_HOST')
    port = os.environ.get('POSTGRES_PORT')
    user = os.environ.get('POSTGRES_USER')
    password = os.environ.get('POSTGRES_PASSWORD')
    db = os.environ.get('POSTGRES_DB')
    url = f"postgresql://{user}:{password}@{host}:{port}/{db}"
    engine = create_engine(url)

    # Create table
    data_dict = {'customers': './data/customers.csv',
                 'products': './data/products.csv', 'sales': './data/sales.csv'}
    for table_name, file_path in data_dict.items():
        df = pd.read_csv(file_path)
        df.to_sql(table_name, con=engine.connect(),
                  index=False, if_exists='replace')

if __name__ == '__main__':
    inject_data()