# import streamlit as st
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_google_genai import  ChatGoogleGenerativeAI
# from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate,MessagesPlaceholder
# from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
# from langchain_core.output_parsers import StrOutputParser
# from langchain_core.runnables import RunnableLambda
# from langchain_core.runnables import RunnablePassthrough

# st.markdown('<h1 style="text-align: center; color: white;">Langchain Powered AI Conversational Data Science Tutor</h1>',unsafe_allow_html=True
#             )


# model=ChatGoogleGenerativeAI(model='gemini-2.0-flash-exp',api_key='AIzaSyBhxO_EeEMWhnltEaMCR4AvjNUw2qY7PKc')

# chat_template=ChatPromptTemplate(
#     messages=[
#         SystemMessage(content='You are a data science tutor,' \
#         'You will be given a question from a student and you will provide them with a detailed answer.' \
#         'You will provide them with a code snippet if they ask you to do that'),
#         HumanMessagePromptTemplate.from_template('{human_input}'),
#         MessagesPlaceholder(variable_name='chat_history',optional=True)
#     ])

# output_parser=StrOutputParser()

# memory_buffer={'history':[]}

# def get_history_from_buffer(human_input):
#     return memory_buffer['history']

# runnable_get_history_from_buffer=RunnableLambda(get_history_from_buffer)

# chain=RunnablePassthrough.assign(chat_history=runnable_get_history_from_buffer)|chat_template|model|output_parser

# inp=st.chat_input('Enter your question')

# if inp:
#     query = {'human_input': inp}
#     response = chain.invoke(query)
    
#     memory_buffer['history'].append(HumanMessage(content=query['human_input']))
#     memory_buffer['history'].append(AIMessage(content=response))

#     # Display both user and AI messages
#     for message in memory_buffer['history']:
#         if isinstance(message, HumanMessage):
#             st.chat_message("user").write(message.content)
#         elif isinstance(message, AIMessage):
#             st.chat_message("assistant").write(message.content)
    


import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import  ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate,MessagesPlaceholder
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda
from langchain_core.runnables import RunnablePassthrough

st.markdown('<h1 style="text-align: center; color: white;">Langchain Powered AI Conversational Data Science Tutor</h1>',unsafe_allow_html=True
            )


model=ChatGoogleGenerativeAI(model='gemini-2.0-flash-exp',api_key='AIzaSyBhxO_EeEMWhnltEaMCR4AvjNUw2qY7PKc')

chat_template=ChatPromptTemplate(
    messages=[
        SystemMessage(content='You are a data science tutor,' \
        'You will be given a question from a student and you will provide them with a detailed answer.' \
        'You will provide them with a code snippet if they ask you to do that'),
        HumanMessagePromptTemplate.from_template('{human_input}'),
        MessagesPlaceholder(variable_name='chat_history',optional=True)
    ])

output_parser=StrOutputParser()

memory_buffer={'history':[]}

def get_history_from_buffer(human_input):
    return memory_buffer['history']

runnable_get_history_from_buffer=RunnableLambda(get_history_from_buffer)

chain=RunnablePassthrough.assign(chat_history=runnable_get_history_from_buffer)|chat_template|model|output_parser

inp=st.chat_input('Enter your question')

if inp:
    query = {'human_input': inp}
    response = chain.invoke(query)
    
    memory_buffer['history'].append(HumanMessage(content=query['human_input']))
    memory_buffer['history'].append(AIMessage(content=response))

    # Display both user and AI messages
    for message in memory_buffer['history']:
        if isinstance(message, HumanMessage):
            st.chat_message("user").write(message.content)
        elif isinstance(message, AIMessage):
            st.chat_message("assistant").write(message.content)
    



