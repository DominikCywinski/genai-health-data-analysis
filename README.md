# GenAI Solution for Conducting Health Data Analysis

## Application Description

This application utilizes the **Gemini Pro** model with added **instruction-tuning** to provide context-aware
responses to health-related queries. The system allows users to input questions, which are then analyzed based on a
provided health dataset to generate insights and recommendations. The project includes an automated CI/CD pipeline 
for seamless builds and tests, as well as unit tests to ensure the reliability and accuracy of the model.

Key features of the application:

- Generating SQL queries to fetch relevant data from an SQLite database using the GenAI model.
- Generating natural language responses based on SQL query result and users question.
- Collecting evaluation metrics such as BLEU, SQL query validity and execution score
- A web interface built using the **Streamlit** framework.
- Protecting user privacy by encrypting patient data.
- CI/CD Pipeline automatically builds and tests the application with each push to the repository or pull request.

## Technologies

- **Gemini Pro** (GenAI model) with **instruction-tuning**.
- **SQLite** for database management.
- **Streamlit** with **caching** for building the web interface.
- **Fernet Encryption** for ensuring patient data privacy.

---

## Setup and Installation

### 1. Clone the repository (skip if you already have it locally):

```bash
git clone https://github.com/DominikCywinski/genai-health-data-analysis.git
cd genai-health-data-analysis
```

### 2. Create .env file with GOOGLE_API_KEY and ENCRYPTION_KEY environment variables.

### 3. If you don’t have conda installed, download and install Miniconda or Anaconda.

### 4. Set Up a Virtual Environment

```bash
conda env create -f environment.yml
```

## Run the Application locally

### 1. Activate conda env:

```bash
conda activate genai-env
```

### 2. Start a local web server:

```bash
streamlit run app.py
```

### 3. The application will be available at the local address provided by Streamlit (usually http://localhost:8501).

### 4. Ask the question i.e.:

```bash
How many women make more than 30000 steps per day?
```

### 5. Run evaluation (optional step):

```bash
python -m src.evaluate
```

Results will be stored in `./evaluation_results/eval_results.csv`.

## Examples

- User Question: `How many women make more than 30000 steps per day?`

- Generated SQL Query:
  `
  SELECT COUNT(*)
  FROM dataset1 AS t1 
  INNER JOIN dataset2 AS t2 
  ON t1.Patient_Number = t2.Patient_Number 
  WHERE t2.Median_Steps_10_days > 30000 
  AND t1.Sex = 1
  `

- SQL Query result: `(134,)`.

- Final response: `134 women make more than 30,000 steps per day.`


- User Question: `Give me average salt content in the diet in mg for obese patients.`

- Generated SQL Query: `SELECT AVG(salt_content_in_the_diet) FROM dataset1 WHERE BMI_category = 'Obese'`;

- SQL Query result: `(25213.509765625,)`.

- Final response: `The average salt content in the diet for obese patients is 25213.51 mg.`

## Features

### 1. Data Processing (optional)

Preprocessing of the dataset can be performed to improve query accuracy i.e. missing data handling, feature engineering.
Based on Data Audit Report stored in `docs/data-audit-report.ipynb`

### 2. Database creation

The SQLite database is automatically created by processing all `.xlsm` files located in the `/datasets` folder. Each
file is parsed, and the data is stored as seperated tables within the database, enabling dynamic queries during runtime.

### 3. SQL Query Generation

The Gemini 1.5 Flash model generates SQL queries based on users question.
SQL queries are then executed on the SQLite database.
The system joins data temporarily on the fly to retrieve the necessary information.

### 4. Natural Language Response Generation

After executing the SQL query, the GenAI model generates a natural language response.
The response is then presented to the user in a readable format.

### 5. Privacy Protection

The application uses Fernet encryption for the Patient_Name external column to ensure privacy.
All user queries are logged and stored in `/logs` to monitor interactions.

### 6. Evaluation

The quality of responses is evaluated with short test set using:

- SQL query validity: Ensures that the generated SQL query is functional and correct.
- BLEU score: Evaluates the quality of generated responses by comparing them to reference responses.
- Execution score: Measures how well the SQL query performs.

## License

This project is licensed under the MIT License.
