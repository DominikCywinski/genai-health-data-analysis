### script responsible for running the web application ###

import streamlit as st
import os
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
from sql_database import execute_sql_query, create_db
from preprocess_data import preprocess_and_return_datasets
from utils import DATABASE_DIR, get_dataframes
from model import SQLResponseGenerator
from web_layout import create_layout
from query_logger import log_query


# Create database if it doesn't exist or overwrite if update button is clicked
def create_or_overwrite_database(overwrite=False):
    if overwrite or not os.path.exists(DATABASE_DIR):
        print("Creating database...")
        dataframes = get_dataframes()
        # optional step for preprocessing and feature engineering
        dataframes[0], dataframes[1] = preprocess_and_return_datasets(
            dataframes[0], dataframes[1]
        )

        create_db(dataframes)
        # Clear cache
        st.cache_resource.clear()


def show_results(response):
    st.subheader("Result:")
    st.header(response)
    print("Result: ", response)


# Load model in cache
@st.cache_resource
def load_model():
    model = SQLResponseGenerator()
    print("Model Loaded")

    return model


# Cache user input and generated SQL query to it
@st.cache_resource
def process_user_input(user_input):
    sql_query = sql_model.generate_sql_query(user_input)
    print(f"Generated SQL Query: {sql_query}")

    sql_results = execute_sql_query(sql_query)
    response = sql_model.generate_natural_language_response(sql_results, user_input)
    return sql_query, response


# Create page layout
user_input, submit_clicked, overwrite_db = create_layout()

create_or_overwrite_database(overwrite=overwrite_db)
sql_model = load_model()

if submit_clicked:
    if user_input != "":
        try:
            # Process user input or get from cache
            sql_query, response = process_user_input(user_input)
            # print result
            show_results(response)
            # Save logs for privacy monitoring
            log_query(user_input, sql_query, response)

        except Exception as e:
            st.header("Sorry, something went wrong :(. Please try again.")
            print(e)
    else:
        st.header("Please enter a question.")
