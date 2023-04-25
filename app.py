import streamlit as st 
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain 
from langchain.memory import ConversationBufferMemory

# App framework
st.set_page_config(page_title='Ask The DB', page_icon='❓',
                   layout='centered', initial_sidebar_state='auto')

st.title('❓ Ask The DB')

st.write('Please use the following format for defining schemas:')
st.write('< Table Name > ( < Column Name > , < Column Name > , ... ); ...')
st.write('Example: Users (ID, Name, Email, Address); Orders (ID, User ID, Amount)')

schema = st.text_input('What is the schema of related tables?')
question = st.text_input('Ask your question to the database!')

# Prompt templates
sql_translation_template = PromptTemplate(
    input_variables = ['schema', 'question'], 
    template='''
             My database has the following schema: {schema} \n \
             I want to know the answer to the following question: {question}. \n \
             Write a SQL query that will answer my question. \n \
             Only return the sql query itself without any surrounding text.
             '''
)

# Llms
llm = OpenAI(temperature=0.5) 
sql_translation_chain = LLMChain(llm=llm, prompt=sql_translation_template)

# Show stuff to the screen if there's a prompt
if schema and question: 
    sql_query = sql_translation_chain.run(schema=schema, question=question)
    st.write(sql_query)
