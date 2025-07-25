import streamlit as st
import openai
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate





import os
from dotenv import load_dotenv


load_dotenv()



##langsmith tracking
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACKING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT")


##prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant that answers questions about the LangChain project."),
        ("user","Question:{question}"),
    ]
)

def generate_response(question, api_key, llm,temperature,max_tokens):
    openai.api_key = api_key
    llm = ChatOpenAI(model="llm", temperature=0.2)
    output_parser = StrOutputParser()
    chain= prompt | llm | output_parser
    response = chain.invoke({"question": question})
    return response

##title of the app
st.title("Q&A Chatbot with OpenAI")

##sidebar for settings
st.sidebar.title("Settings")    
api_key = st.sidebar.text_input("OpenAI API Key", type="password")

##deop down to select various llm models
llm = st.sidebar.selectbox(
    "Select LLM Model",
    ["gpt-3.5-turbo", "gpt-4"]
)

#adjust temperature and max tokens
temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.7)
max_tokens = st.sidebar.slider("Max Tokens", 50, 300, 150)

#main interface for user input
st.write("Go ahead and ask any question:")
user_input= st.text_input("Your Question")

if user_input:
    response = generate_response(user_input, api_key, llm, temperature, max_tokens)
    st.write("Response:")
    st.write(response)
else:
    st.write("Please enter a question to get a response.")