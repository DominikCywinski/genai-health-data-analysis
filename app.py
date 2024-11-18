### script responsible for running the web application ###

import streamlit as st
import os
from src.sql_database import execute_sql_query, create_db
from src.preprocess_data import preprocess_and_return_datasets
from src.utils import DATABASE_DIR, get_dataframes
from src.model import SQLResponseGenerator
from src.web_layout import create_layout
from src.query_logger import log_query


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


# Create page layout
user_input, submit_clicked, overwrite_db = create_layout()

create_or_overwrite_database(overwrite=overwrite_db)

# Check if model is initialized in session state
if "sql_generator" not in st.session_state:
    st.session_state["sql_generator"] = SQLResponseGenerator()
    print("Model created")

# Get SQL model from session state
sql_model = st.session_state["sql_generator"]

if submit_clicked:
    if user_input != "":
        try:
            sql_query = sql_model.generate_sql_query(user_input)
            print(f"Generated SQL Query: {sql_query}")

            sql_results = execute_sql_query(sql_query)
            response = sql_model.generate_natural_language_response(
                sql_results, user_input
            )

            st.subheader("Result:")
            st.header(response)
            print("Result: ", response)
            # Save logs for privacy monitoring
            log_query(user_input, sql_query, response)
        except Exception as e:
            st.header("Sorry, something went wrong :(. Please try again.")
            print(e)
    else:
        st.header("Please enter a question.")
