import pandas as pd
from sqlalchemy import create_engine
from typing import List, Dict

class DBConnector():
    def __init__(self, dialect: str, host: str, port: int, username: str, password: str, database: str,) -> None:
        self.engine = create_engine(f'{dialect}://{username}:{password}@{host}:{port}/{database}')

    def execute_query(self, query: str) -> pd.DataFrame:
        with self.engine.connect() as connection:
            return pd.read_sql(query, connection)

    def read_schema(self) -> List[Dict[str, Dict[str, str]]]:
        query_results = self.execute_query("SELECT table_name, column_name, data_type \
                                      FROM information_schema.columns \
                                      WHERE table_schema = 'public'")
        
        schema = query_results.groupby('table_name')\
                         .apply(lambda x: x.set_index('column_name')['data_type'].to_dict())\
                         .to_dict()
        
        return schema
    
    def schema_to_text(self, schema: List[Dict[str, Dict[str, str]]]) -> str:
        schema_str = ''
        for table_name, column_dict in schema.items():
            schema_str += f'{table_name} ('
            for column_name, column_type in column_dict.items():
                schema_str += f'{column_name} {column_type}, '
            schema_str = schema_str[:-2] + '); '
        return schema_str
    
    def get_schema_text(self) -> str:
        schema = self.read_schema()
        schema_text = self.schema_to_text(schema)
        return schema_text

    