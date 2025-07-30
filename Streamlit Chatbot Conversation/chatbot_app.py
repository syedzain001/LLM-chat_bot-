from dotenv import load_dotenv
import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
import os

load_dotenv()

os.environ["OPENAI_API_KEY"]=os.getenv("OPENAI_API_KEY")




# Load LLM
llm = OpenAI(temperature=0.7)

# Session states
if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

if "clarify_count" not in st.session_state:
    st.session_state.clarify_count = 0

if "messages" not in st.session_state:
    st.session_state.messages = []

if "followup_asked" not in st.session_state:
    st.session_state.followup_asked = False

# Clarification prompt
clarify_prompt = PromptTemplate(
    input_variables=["chat_history", "user_input"],
    template="""
You are a helpful assistant. The conversation so far is:

{chat_history}

The user just asked: "{user_input}"

Your task:

- If the user's question is clear and complete, respond only with: NO_CLARIFICATION_NEEDED
- If the question is ambiguous or incomplete, respond with a helpful clarifying question.

ONLY respond with either:
- NO_CLARIFICATION_NEEDED
- or one clarifying question
"""
)

clarify_chain = LLMChain(llm=llm, prompt=clarify_prompt, memory=st.session_state.memory)

# Answer prompt
answer_prompt = PromptTemplate(
    input_variables=["chat_history", "user_input"],
    template="""
You are a helpful assistant.

The conversation so far:
{chat_history}

User just asked: "{user_input}"

Give a complete and helpful answer.
"""
)
answer_chain = LLMChain(llm=llm, prompt=answer_prompt, memory=st.session_state.memory)

# Follow-up (without memory)
followup_prompt = PromptTemplate(
    input_variables=["chat_history"],
    template="""
You are an assistant evaluating if a user's question has been fully answered.

Chat:
{chat_history}

Has the main question been fully answered?

If yes, return exactly: ANSWER_COMPLETE  
If not, return one helpful follow-up question to guide the user.

Respond ONLY with:
- ANSWER_COMPLETE
- or a follow-up question
"""
)
followup_chain = LLMChain(llm=llm, prompt=followup_prompt, memory=None)

# UI
st.title("?? Smart AI Chatbot with Clarification & Memory")
user_input = st.chat_input("Ask me anything...")

if user_input:
    # Reset follow-up asked
    st.session_state.followup_asked = False

    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.memory.chat_memory.add_user_message(user_input)

    # Step 1: Clarification
    clarification = clarify_chain.predict(user_input=user_input).strip()

    if clarification != "NO_CLARIFICATION_NEEDED" and st.session_state.clarify_count < 3:
        st.session_state.clarify_count += 1
        st.session_state.messages.append({"role": "assistant", "content": clarification})
        st.session_state.memory.chat_memory.add_ai_message(clarification)
    else:
        # Reset clarify count
        st.session_state.clarify_count = 0

        # Step 2: Answer
        answer = answer_chain.predict(user_input=user_input).strip()
        st.session_state.messages.append({"role": "assistant", "content": answer})
        st.session_state.memory.chat_memory.add_ai_message(answer)

        # Step 3: Follow-up (only once)
        if not st.session_state.followup_asked:
            chat_history = st.session_state.memory.load_memory_variables({})["chat_history"]
            followup = followup_chain.predict(chat_history=chat_history).strip()

            if followup != "ANSWER_COMPLETE":
                st.session_state.messages.append({"role": "assistant", "content": followup})
                st.session_state.memory.chat_memory.add_ai_message(followup)

            st.session_state.followup_asked = True

# Render all messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
