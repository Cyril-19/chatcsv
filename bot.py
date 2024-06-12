import os
from dotenv import load_dotenv
import pandas as pd
from pandasai import SmartDataframe
from pandasai import Agent
import streamlit as st

# Load environment variables (assuming PANDASAI_API_KEY is set)
load_dotenv()
api_key = os.getenv("PANDASAI_API_KEY")

# Initialize conversation history as an empty list
conversation_history = []

def chat_with_csv(df, prompt):
    agent = Agent(SmartDataframe(df))
    result = agent.chat(prompt)

    conversation_history.append((prompt, result))

    return result

def display_conversation_history():
    if conversation_history:
        st.header("Conversation History")
        for user_prompt, ai_response in conversation_history:
            # Separate user queries and AI responses for clarity
            st.write(f"**You:** {user_prompt}")
            st.write(f"**Me:** {ai_response}")
    else:
        st.info("No conversation history yet.")

st.set_page_config(layout="wide")

st.title("ChatCSV")

# Ensure that session state is initialized
if "messages" not in st.session_state:
    st.session_state.messages = []

input_csv = st.file_uploader("Upload your CSV file", type=["csv"])

if input_csv is not None:
    col1, col2 = st.columns([1, 1])

    with col1:
        st.info("CSV Uploaded Successfully")
        data = pd.read_csv(input_csv)
        st.dataframe(data, use_container_width=True)

    with col2:
        input_container = st.container()
        chat_container = st.container()
        

        # Display chat messages from history on app rerun
# Display chat messages
        with input_container:
            prompt = st.text_input("Ask a question about your data:")
            if prompt:
                # Add user message to chat history
                st.session_state.messages.append({"role": "user", "content": prompt})
                # Display user message in chat message container
                with chat_container:
                    with st.chat_message("user"):
                        st.markdown(prompt)

                # Display assistant response in chat message container
                with chat_container:
                    with st.chat_message("assistant"):
                        response = chat_with_csv(data, prompt)
                        st.markdown(response)
        with chat_container:
            chat_expander = st.expander("Chat History", expanded=True)
            with chat_expander:
                for message in st.session_state.messages:
                    with st.chat_message(message["role"]):
                        st.markdown(message["content"])

      
        
           
                
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": response})
            # display_conversation_history()
else:
    st.info("Please upload a CSV file to start chatting.")
