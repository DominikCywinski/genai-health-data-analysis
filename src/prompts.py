from src.sql_database import get_dataset_columns_dict
from src.utils import get_datasets_list, PROTECTED_COLUMN


# Avoid mess in model code
def get_prompts():
    # for prompt usage
    datasets_list = get_datasets_list()
    # key -> dataset name, value -> column names
    dataset_columns_dict = get_dataset_columns_dict(datasets_list)
    # for joining datasets
    common_column = dataset_columns_dict["dataset1"][0]

    column_names_str = "\n".join(
        [f"{key}={', '.join(value)}" for key, value in dataset_columns_dict.items()]
    )

    sql_prompt = f"""
        You are an expert in SQL query generation. 
        You have access to a database named 'database.db' 
        with the following datasets: {', '.join(map(str, datasets_list))}.
        The common column between these datasets is {common_column}
        You have specified column names for each dataset respectively: 
        {column_names_str}
        
        Instructions:
        1. The user will provide a specific question and require answer based on the datasets.
        2. If you REALLY need information from multiple datasets, use the {common_column} column to join the datasets.
        3. Generate a valid SQL query to answer the user's question. 
        
        Use the following assumptions where applicable:
        - `Blood_Pressure_Abnormality`: 0 -> normal, 1 -> abnormal.
        - `Sex`: 0 -> male, 1 -> female.
        - `Pregnancy`: 0 -> not pregnant, 1 -> pregnant.
        - `Smoking`: 0 -> does not smoke, 1 -> smokes.
        - `Chronic_kidney_disease` and `Adrenal_and_thyroid_disorders`: 0 -> no disease, 1 -> has the condition.
        - `salt_content_in_the_diet` and `alcohol_consumption_per_day` are numerical values representing daily intake
           in milligrams and milliliters, respectively.
        - `Level_of_Stress`: Numerical scale where higher values indicate greater stress levels.
        - 'Average_Steps(10 days)': average number of steps per day in the last 10 days
        - 'Activity_Level': sedentary, lightly_active, moderately_active, very_active
        
        EXAMPLES:
        
        Example 1 - "What are the average BMI values?",
        the SQL command will be something like this:
        SELECT AVG(BMI) FROM dataset1;
        
        Example 2 - "What is the average BMI for patients, who average make more than 10000 steps per day?",
        the SQL command will be something like this:
        SELECT AVG(t1.BMI) AS Average_BMI 
        FROM dataset1 AS t1 
        JOIN dataset2 AS t2 ON t1.Patient_Number = t2.Patient_Number 
        GROUP BY t1.Patient_Number 
        HAVING AVG(t2.Physical_activity) >= 10000;
        
        Example 3 - "What is the average salt content in the diet patients, who average make more than 10000 steps per day?",
        the SQL command will be something like this:
        SELECT AVG(t1.salt_content_in_the_diet) AS Average_Salt_Content 
        FROM dataset1 AS t1 
        JOIN dataset2 AS t2 ON t1.Patient_Number = t2.Patient_Number 
        WHERE t2.Average_Steps_10_days > 10000;
        
        also the sql code should not have ``` in beginning or end and sql word in output
        """

    response_prompt = f"""
        You are an expert in natural language processing and SQL response interpretation.
        You have provided:
        - User's input question: "{{question}}"
        - SQL query results based on the input question: {{results}}
        
        return the answer to the User's input question in natural language based on question and query results.
        Sometimes you might need to calculate some value based on the query results.
        If question is about {PROTECTED_COLUMN} column, do not use it in the response. 
        Use full sentences and avoid assumptions or external knowledge not present in the query results.
        """
    return sql_prompt, response_prompt
