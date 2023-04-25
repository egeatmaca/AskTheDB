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
                    My database has the following schema: \n {schema} \n\n \
                    I want to know the answer to the following question: {question}. \n \
                    Write a SQL query that will answer my question. \n\n \
                    Only return the sql query itself without any surrounding text.
                    '''
        )

        
        self.llm = OpenAI(temperature=0.5)

        self.chain = LLMChain(llm=self.llm, prompt=self.template)

    def translate(self, question, schema):
        return self.chain.run(question=question, schema=schema)
