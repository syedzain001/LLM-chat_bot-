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

2.streamlit_LangChain Assist:

This is an AI-powered chatbot built using Streamlit and LangChain.
It uses OpenAI's GPT model with memory and clarification logic.
Loads API keys securely via .env using python-dotenv.
Initializes memory using ConversationBufferMemory to track chat history.
Clarifies ambiguous user inputs before answering (max 3 attempts).
Uses LLMChain with custom prompts for clarification, answering, and follow-ups.
Detects if the user question was fully answered and suggests follow-ups if needed.
Maintains session state across multiple inputs for coherent conversations.
All interactions are displayed dynamically in Streamlit’s chat UI.
Ideal for building smart, interactive assistant portals.
