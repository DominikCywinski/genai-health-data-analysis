### Script responsible for creating database and executing SQL queries ###

import sqlite3
from utils import DATABASE_DIR, PROTECTED_COLUMN
from encrypt import encrypt_value, decrypt_value


def create_db(datasets_list):

    connection = sqlite3.connect(DATABASE_DIR)

    # Create table in database for all datasets in DATABASE_DIR
    for idx, dataset in enumerate(datasets_list):
        # Encrypt Patient Number to secure the data
        dataset[PROTECTED_COLUMN] = dataset[PROTECTED_COLUMN].apply(encrypt_value)

        # Keep idx+1 as table name according to datasets names (to avoid missunderstanding)
        dataset.to_sql(f"dataset{idx+1}", connection, if_exists="replace", index=False)

    connection.close()


# Return a dictionary from db with dataset names as keys and column names as values
def get_dataset_columns_dict(datasets_list):
    connection = sqlite3.connect(DATABASE_DIR)
    dataset_columns_dict = {}

    for idx, dataset in enumerate(datasets_list):
        cursor = connection.cursor()
        cursor.execute(f"PRAGMA table_info(dataset{idx+1});")
        columns = [column[1] for column in cursor.fetchall()]
        dataset_columns_dict[f"dataset{idx+1}"] = columns

    connection.close()

    return dataset_columns_dict


def execute_sql_query(sql_query):
    connection = sqlite3.connect(DATABASE_DIR)

    cursor = connection.cursor()
    cursor.execute(sql_query)

    results = cursor.fetchall()

    connection.commit()
    connection.close()

    for row in results:
        print(row)

    return results
