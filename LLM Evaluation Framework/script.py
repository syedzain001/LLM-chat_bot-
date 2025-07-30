import pandas as pd

# Load the CSV file with question, answer key, and marks
file_path = "data\questionAndAnswers.txt"
df = pd.read_csv(file_path)

# Example of how your DataFrame looks
print(df.head())