### Optional step script ###
### BASED ON 'data-audit-report.ipynb' ###

import pandas as pd

# pd.set_option("display.max_columns", None)


# Return preprocessed datasets
def get_preprocessed_datasets(dataset1, dataset2):
    # read datasets
    dataset1 = pd.read_excel(dataset1)
    dataset2 = pd.read_excel(dataset2)

    check_missing_data(dataset1, dataset2)

    # fill missing data in dataset1
    dataset1.fillna(
        {
            "Genetic_Pedigree_Coefficient": dataset1[
                "Genetic_Pedigree_Coefficient"
            ].median(),
            "Pregnancy": 0,
            "alcohol_consumption_per_day": dataset1[
                "alcohol_consumption_per_day"
            ].median(),
        },
        inplace=True,
    )

    # replace physical activity with median
    dataset2 = (
        dataset2.groupby("Patient_Number")["Physical_activity"]
        .median()
        .reset_index()
        .astype(int)
    )
    dataset2 = dataset2.rename(columns={"Physical_activity": "Median_Steps_10_days"})

    check_missing_data(dataset1, dataset2)

    ## replace binary with Male/Female for better understanding
    # dataset1["Sex"] = dataset1["Sex"].replace({1: "Female", 0: "Male"})

    dataset1, dataset2 = feature_engineering(dataset1, dataset2)

    return [dataset1, dataset2]


# For testing purpose: Check if there is any missing data in df1 and df2
def check_missing_data(df1, df2):
    if df1.isnull().sum().sum() + df2.isnull().sum().sum() == 0:
        print("\033[32mNo missing data\033[0m")
    else:
        print("\033[31mMissing data!!!\033[0m")


def feature_engineering(dataset1, dataset2):
    # Dataset1
    # Age group
    bins = [0, 18, 25, 35, 45, 55, 65, 75, 100]
    labels = ["0-18", "19-25", "26-35", "36-45", "46-55", "56-65", "66-75", "76-100"]
    dataset1["Age_group"] = pd.cut(
        dataset1["Age"], bins=bins, labels=labels, right=False
    )

    # BMI category
    bins = [0, 18.5, 24.9, 29.9, float("inf")]
    labels = ["Underweight", "Normal", "Overweight", "Obese"]
    dataset1["BMI_category"] = pd.cut(
        dataset1["BMI"], bins=bins, labels=labels, right=False
    )

    # Dataset2
    # Activity level
    bins = [0, 5000, 7500, 10000, float("inf")]
    labels = ["sedentary", "lightly_active", "moderately_active", "very_active"]

    dataset2["Activity_Level"] = pd.cut(
        dataset2["Median_Steps_10_days"], bins=bins, labels=labels, right=False
    )
    return dataset1, dataset2
