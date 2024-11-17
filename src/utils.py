import os
import pandas as pd

DATABASE_DIR = "databases/database.db"

DATASETS_DIR = "datasets/"


def get_datasets_list():
    datasets_list = []
    for file in os.listdir(DATASETS_DIR):
        if file.endswith(".xlsm") and not file.startswith("~$"):  # avoid hidden files
            datasets_list.append(os.path.join(DATASETS_DIR, file))

    return datasets_list


def get_dataframes():
    datasets = get_datasets_list()
    dfs = [pd.read_excel(dataset, engine="openpyxl") for dataset in datasets]

    return dfs
