import os
import google.generativeai as genai
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from src.prompts import get_prompts
from src.sql_database import execute_sql_query


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
        self.llm = genai.GenerativeModel("gemini-1.5-flash")

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


# For TESTING purpose
# model = SQLResponseGenerator()
# question = "how many people with blood presure have bmi larger than 45?"
# sql_query = model.generate_sql_query(question)
# print(f"Generated SQL Query: {sql_query}")
# sql_query = "SELECT AVG(t1.salt_content_in_the_diet) AS Average_Salt_Content FROM dataset1 AS t1 JOIN dataset2 AS t2 ON t1.Patient_Number = t2.Patient_Number WHERE t2.Average_Steps_10_days > 10000;"
# sql_results = execute_sql_query(sql_query)
# print(sql_results)
# response = model.generate_natural_language_response(sql_results, question)
# print(response)
