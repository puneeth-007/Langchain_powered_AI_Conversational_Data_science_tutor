import os

os.makedirs("chats_data", exist_ok=True)
import streamlit as st
import uuid
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_community.chat_message_histories import SQLChatMessageHistory

# Title
st.markdown('<h1 style="text-align: center; color: white;">LangChain Powered AI Conversational Data Science Tutor</h1>', unsafe_allow_html=True)

# Session ID for persistent memory
if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# Define how to load chat history from SQLite
def get_session_message_history_from_db(session_id):
    return SQLChatMessageHistory(
        session_id=session_id,
        connection_string="sqlite:///chats_data/sqlite.db"
    )

# Define model
model = ChatGoogleGenerativeAI(
    model='gemini-2.0-flash-exp',
    api_key=os.environ["gemapi"] 
)

# Prompt template
chat_template = ChatPromptTemplate(
    messages=[
        SystemMessage(content="You are a data science tutor. You will provide detailed answers and code snippets when asked."),
        HumanMessagePromptTemplate.from_template('{human_input}'),
        MessagesPlaceholder(variable_name='chat_history', optional=True)
    ]
)

output_parser = StrOutputParser()

chain = RunnableWithMessageHistory(
         chat_template | model | output_parser,
         get_session_history=get_session_message_history_from_db,
         input_messages_key="human_input",
         history_messages_key="chat_history"
     )

st.sidebar.markdown(f"**💾 Session ID:** `{st.session_state.session_id}`")
st.sidebar.caption("Save this ID to view this conversation again.")
inp = st.chat_input("Ask me anything about data science")
session_id_input = st.sidebar.text_input("🔍 Enter session ID to view history")

if session_id_input:
    past_history = get_session_message_history_from_db(session_id_input)
    st.sidebar.markdown("### Chat History")
    for msg in past_history.messages:
        role = "user" if isinstance(msg, HumanMessage) else "assistant"
        st.sidebar.markdown(f"**{role.capitalize()}:** {msg.content}")

if inp:
    # Append user message to DB
    history = get_session_message_history_from_db(st.session_state.session_id)
    history.add_user_message(inp)


    # Invoke the model
    response = chain.invoke(
        {"human_input": inp},
        config={"configurable": {"session_id": st.session_state.session_id}}
    )

    #Append assistant response to DB
    history.add_ai_message(response)

import sqlite3

# Path to your SQLite database
db_path = "chats_data/sqlite.db"

# SQL to delete duplicate messages (keep the first occurrence)
dedupe_sql = """
DELETE FROM message_store
WHERE rowid NOT IN (
    SELECT MIN(rowid)
    FROM message_store
    GROUP BY session_id,message
);
"""

# Run the deduplication
def remove_duplicates():
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(dedupe_sql)
        conn.commit()

    except sqlite3.Error as e:
        conn.rollback()

    finally:
        conn.close()

# Call the function
remove_duplicates()

# Display entire conversation from DB
for msg in get_session_message_history_from_db(st.session_state.session_id).messages:
    role = "user" if isinstance(msg, HumanMessage) else "assistant"
    st.chat_message(role).write(msg.content)


