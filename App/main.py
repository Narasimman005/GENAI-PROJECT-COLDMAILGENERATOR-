import streamlit as st
from utils import clean_text
from langchain_community.document_loaders.web_base import WebBaseLoader
from portfolio import Portfolio
from chains import Chain
def create_st_app(llm, portfolio, clean_text):
    st.title("Cold Mail Generator")
    inp = st.text_input("Enter the URL")
    btn = st.button("Submit")
    if btn:
        try:
            loader = WebBaseLoader(inp)
            data = clean_text(loader.load().pop().page_content)
            portfolio.load_data()
            jobs=llm.extract_jobs(data)
            for job in jobs:
                skills = job.get('skills', [])
                links=portfolio.query_data(skills)
                #links_text = "".join(links)
                email=llm.write_mail(job, links)
                st.code(email.content, language="markdown")
        except Exception as e:
            st.error(f"An error: {e}")

if __name__=="__main__":
    llm = Chain()
    portfolio = Portfolio()
    #st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    create_st_app(llm, portfolio, clean_text)
