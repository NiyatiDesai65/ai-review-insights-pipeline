import os

folders = [
    "src/ingestion",
    "src/processing", 
    "src/ai",
    "src/reporting",
    "include/raw",
    "include/results",
    "logs",
    "tests",
]

init_files = [
    "src/__init__.py",
    "src/ingestion/__init__.py",
    "src/processing/__init__.py",
    "src/ai/__init__.py",
    "src/reporting/__init__.py",
]

empty_files = [
    "config.py",
    "tests/test_cleaner.py",
    "src/ingestion/kaggle_reader.py",
    "src/processing/cleaner.py",
    "src/ai/analyzer.py",
    "src/reporting/reporter.py",
    "dags/amazon_review_dag.py",
    "logs/.gitkeep",
    "include/raw/.gitkeep",
    "include/results/.gitkeep",
]

# create folders
for folder in folders:
    os.makedirs(folder, exist_ok=True)
    print(f"created folder: {folder}")

# create init files
for f in init_files:
    with open(f, 'w') as file:
        file.write("")
    print(f"created: {f}")

# create empty files
for f in empty_files:
    with open(f, 'w') as file:
        file.write("")
    print(f"created: {f}")

print("\nProject structure created successfully.")