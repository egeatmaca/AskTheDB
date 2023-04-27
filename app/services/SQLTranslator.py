from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os


class SQLTranslator:
    def __init__(self, api_key=None):
        if api_key:
            os.environ['OPENAI_API_KEY'] = api_key

        
        self.template = PromptTemplate(
            input_variables=['question', 'schema'],
            template='''
                    My SQL database has a schema with the following tables and fields: \n {schema} \n\n \
                    I want to know: {question}. \n \
                    Write a SQL query for what I want to know. \n\n \
                    Return the SQL query in a code block.
                    '''
        )

        
        self.llm = OpenAI(temperature=0.5)

        self.chain = LLMChain(llm=self.llm, prompt=self.template)

    def translate(self, question, schema):
        return self.chain.run(question=question, schema=schema)
