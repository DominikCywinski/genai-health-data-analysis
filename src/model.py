import os
import google.generativeai as genai
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from prompts import get_prompts


# Model responsible for generating SQL queries and replying to user based on SQL results and user question
class SQLResponseGenerator:
    def __init__(self, api_key=None):
        load_dotenv()  # Load environment keys
        if api_key is None:
            api_key = os.getenv("GOOGLE_API_KEY")
        genai.configure(api_key=api_key)
        # get prompts
        sql_prompt, response_prompt = get_prompts()

        self.sql_prompt = sql_prompt
        self.response_prompt = response_prompt
        self.llm = genai.GenerativeModel("gemini-pro")

        self.sql_template = PromptTemplate(
            input_variables=["question"], template=sql_prompt
        )
        self.response_template = PromptTemplate(
            input_variables=["results", "question"], template=response_prompt
        )

    # Generate SQL query based on question
    def generate_sql_query(self, question):
        prompt = self.sql_template.format(question=question)
        response = self.llm.generate_content([prompt, question])

        return response.text

    # Generate response based on SQL query and question
    def generate_natural_language_response(self, results, question):
        prompt = self.response_template.format(results=results, question=question)
        response = self.llm.generate_content([prompt, question])

        return response.text
