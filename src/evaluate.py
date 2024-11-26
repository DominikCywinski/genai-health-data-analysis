### Evaluates SQL queries using metrics such as BLEU, execution score and validity ###
### saves results to a evaluation_results/eval_results.csv file ###

import sqlite3
import pandas as pd
import csv
import sqlparse
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from utils import DATABASE_DIR
from model import SQLResponseGenerator

# Sample test queries for evaluation
test_queries = [
    {
        "input": "How many women are there?",
        "reference_sql": "SELECT COUNT(*) FROM dataset1 WHERE Sex = 1",
        "generated_sql": "",
    },
    {
        "input": "What are the average BMI values?",
        "reference_sql": "SELECT AVG(BMI) FROM dataset1",
        "generated_sql": "",
    },
    {
        "input": "What is the average salt content in the diet patients, who average make more than 10000 steps per day?",
        "reference_sql": "SELECT AVG(t1.salt_content_in_the_diet) AS Average_Salt_Content FROM dataset1 AS t1 JOIN dataset2 AS t2 ON t1.Patient_Number = t2.Patient_Number  WHERE t2.Median_Steps_10_days > 10000",
        "generated_sql": "",
    },
]


# Normalize query
def normalize_sql(sql_query: str) -> str:
    formatted_query = sqlparse.format(
        sql_query.strip(),
        reindent=True,  # Reformat SQL with consistent indentation
        keyword_case="lower",  # Convert SQL keywords to lowercase
    )
    # Remove excessive newlines and trailing spaces
    normalized_query = " ".join(formatted_query.split())

    return normalized_query


def prepare_test_data(model, test_queries):
    for query in test_queries:
        generated_sql = model.generate_sql_query(query["input"])
        query["reference_sql"] = normalize_sql(query["reference_sql"])
        query["generated_sql"] = normalize_sql(generated_sql)

    return test_queries


# Check if SQL syntax is valid
def validate_sql_syntax(sql_query):
    connection = sqlite3.connect(DATABASE_DIR)
    try:
        connection.execute(sql_query)  # Test query on an empty database
        return True
    except Exception as e:
        return False


# Execute generated and reference SQL query and compare if results match
def execute_queries_and_compare(generated_sql, reference_sql):

    try:
        connection = sqlite3.connect(DATABASE_DIR)

        # Execute generated SQL and fetch results
        generated_result = pd.read_sql_query(generated_sql, connection)

        # Execute reference SQL and fetch results
        reference_result = pd.read_sql_query(reference_sql, connection)

        # Close the connection
        connection.close()

        # Compare the two DataFrames
        if generated_result.equals(reference_result):
            return True, {"message": "Results match"}
        else:
            return False, {
                "message": "Results do not match",
                "generated_result": generated_result,
                "reference_result": reference_result,
            }

    except Exception as e:
        return False, {"error": str(e)}


# Calculate BLEU score using reference and generated SQL queries
def calculate_bleu(generated_sql, reference_sql):
    # Tokenize queries (split by spaces)
    generated_tokens = generated_sql.split()
    reference_tokens = reference_sql.split()

    # Wrap reference tokens in a list (BLEU expects a list of references)
    reference_tokens_wrapped = [reference_tokens]

    # Calculate BLEU score with smoothing to avoid zero scores
    bleu_score = sentence_bleu(
        reference_tokens_wrapped,
        generated_tokens,
        smoothing_function=SmoothingFunction().method1,  # avoid zero scores
    )

    return bleu_score


# Evaluates SQL queries using provided metrics and saves results to a CSV file.
def evaluate_and_save_results(test_queries, output_csv_path):
    results = []

    for query in test_queries:
        generated_sql = query["generated_sql"]
        reference_sql = query["reference_sql"]
        user_input = query["input"]

        # Calculate metrics
        is_valid = validate_sql_syntax(generated_sql)
        execution_score = execute_queries_and_compare(generated_sql, reference_sql)
        bleu_score = calculate_bleu(generated_sql, reference_sql)

        # Append results to list
        results.append(
            {
                "User Input": user_input,
                "Generated SQL": generated_sql,
                "Reference SQL": reference_sql,
                "Is Valid": is_valid,
                "Execution Score": execution_score,
                "BLEU Score": bleu_score,
            }
        )

    # Write results to CSV
    with open(output_csv_path, mode="w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=[
                "User Input",
                "Generated SQL",
                "Reference SQL",
                "Is Valid",
                "Execution Score",
                "BLEU Score",
            ],
        )
        writer.writeheader()
        writer.writerows(results)

    print(f"Results saved to {output_csv_path}")


if __name__ == "__main__":
    model = SQLResponseGenerator()

    test_queries = prepare_test_data(model, test_queries)
    evaluate_and_save_results(test_queries, "evaluation_results/eval_results.csv")
