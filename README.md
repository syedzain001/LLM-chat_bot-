 LLM Evaluation Framework:
 
 This project automates student answer sheet evaluation using GPT-4.
It loads question blueprints and student responses from .txt files.
Merges both datasets based on question number (Qno).
Uses GPT-4 API to compare student answers with correct ones.
GPT returns scores for each question without explanations.
Final scores are parsed and stored in the DataFrame.
Aggregates total marks per student (name + USN).
Requires pandas, openai, python-dotenv.
API keys are managed securely via a .env file.
Ideal for automated grading of subjective answers.
