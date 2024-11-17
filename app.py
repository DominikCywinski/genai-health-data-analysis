import streamlit as st
import os
from src.sql_database import execute_sql_query, create_db
from src.preprocess_data import get_preprocessed_datasets
from src.utils import get_datasets_list, DATABASE_DIR
from src.model import SQLResponseGenerator
from src.web_layout import create_layout


# Create database if it doesn't exist or overwrite if button is clicked
def create_or_overwrite_database(overwrite=False):
    if overwrite or not os.path.exists(DATABASE_DIR):
        print("Creating database...")
        datasets = get_datasets_list()
        # optional step for preprocessing and feature engineering
        datasets[0], datasets[1] = get_preprocessed_datasets(datasets[0], datasets[1])
        create_db(datasets)


# Create page layout
user_input, submit_clicked, overwrite_db = create_layout()

create_or_overwrite_database(overwrite=overwrite_db)

# Check if model is initialized
if "sql_generator" not in st.session_state:
    st.session_state["sql_generator"] = SQLResponseGenerator()
    print("Model created")

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

        except Exception as e:
            st.header("Sorry, something went wrong :(. Please try again.")
            print(e)
    else:
        st.header("Please enter a question.")
