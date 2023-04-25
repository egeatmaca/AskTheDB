import streamlit as st 
import json
from services.DBConnector import DBConnector
from services.SQLTranslator import SQLTranslator

class App:
    def __init__(self):
        self.sql_translator = SQLTranslator()
        self.db_connector = None

    def setup_page(self):
        # Set page config
        st.set_page_config(page_title='Ask The DB', page_icon='❓',
                        layout='centered', initial_sidebar_state='auto')

        # Set title
        st.title('❓ Ask The DB')

    def configure_db(self):
        with st.expander('Step 1: Configure the DB', expanded=True):
            db_config_file = st.file_uploader('Upload your database config file.', type='json')
            st.write('For testing with mock data:')
            with open('./sample_config.json', 'r') as sample_config_file:
                st.download_button(label='Download sample config file', data=sample_config_file.read(),
                                file_name='sample_config.json', mime='application/json')
            
            if db_config_file:
                self.db_config = json.load(db_config_file)
                self.db_connector = DBConnector(**self.db_config)
            
    def get_db_schema(self):
        if self.db_connector:
            schema = self.db_connector.read_schema()
            with st.expander('Step 2: View the DB Schema (Optional)'):
                st.write('Schema of your database:')
                st.json(schema, expanded=False)
            self.schema = schema

    def ask_the_db(self):
        if self.db_connector and self.schema:
            # Get question to the db
            question = None
            with st.expander('Step 3: Ask the DB'):
                question = st.text_input('Ask a question to your database!')

            # If a question is entered
            if question:
                # Convert schema to text
                schema_text = self.db_connector.schema_to_text(self.schema)
                # Translate to sql, execute and show results
                sql_query = self.sql_translator.translate(question, schema_text)
                results = self.db_connector.execute_query(sql_query)
                st.write('Results:')
                st.dataframe(results)
        
    def run(self):
        self.setup_page()
        self.configure_db()
        self.get_db_schema()
        self.ask_the_db()


if __name__ == '__main__':
    App().run()