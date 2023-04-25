import streamlit as st 
import json
from services.DBConnector import DBConnector
from services.SQLTranslator import SQLTranslator

# Set page config
st.set_page_config(page_title='Ask The DB', page_icon='❓',
                   layout='centered', initial_sidebar_state='auto')

# Set title
st.title('❓ Ask The DB')

# Get db config file
db_config_file = None
with st.expander('Step 1: Configure the DB', expanded=True):
    db_config_file = st.file_uploader('Upload your database config file.', type='json')
    st.write('For testing with mock data:')
    with open('./sample_config.json', 'r') as sample_config_file:
        st.download_button(label='Download sample config file', data=sample_config_file.read(),
                        file_name='sample_config.json', mime='application/json')
        
# If db config file is uploaded
if db_config_file:
    # Initialize db connector
    db_config = json.load(db_config_file)
    db_connector = DBConnector(**db_config)

    # Get db schema and write it to the screen
    schema_str = None
    schema = db_connector.read_schema()
    schema_str = db_connector.cast_schema_to_string(schema)
    with st.expander('Step 2: View the DB Schema (Optional)'):
        st.write('Schema of your database:')
        st.json(schema, expanded=False)

    # Get question to the db
    question = None
    with st.expander('Step 3: Ask the DB'):
        question = st.text_input('Ask a question to your database!')

    # If a question is entered
    if question:
        # Translate to sql, execute and show results
        sql_query = SQLTranslator().translate(question, schema)
        results = db_connector.execute_query(sql_query)
        st.write('Results:')
        st.dataframe(results)