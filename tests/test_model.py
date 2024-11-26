import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))
from evaluate import validate_sql_syntax
from model import SQLResponseGenerator


def test_model_initialization():
    # Create an instance of the agent
    model = SQLResponseGenerator()
    response = model.generate_sql_query("How many males?")

    assert validate_sql_syntax(response), "The SQL query is not valid."

    print("Test passed successfully.")
