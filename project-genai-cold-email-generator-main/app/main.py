import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from chains import Chain
from portfolio import Portfolio
from utils import clean_text


def create_streamlit_app(llm, portfolio, clean_text):
    st.title("📧 Cold Mail Generator")

    # User input for URL and name
    url_input = st.text_input("Enter a URL:", value="")

    submit_button = st.button("Submit")

    if submit_button:
        if url_input:
            try:
                # Load and clean data from the provided URL
                loader = WebBaseLoader([url_input])
                data = clean_text(loader.load().pop().page_content)

                # Load portfolio and generate email
                portfolio.load_portfolio()
                jobs = llm.extract_jobs(data)

                for job in jobs:
                    skills = job.get('skills', [])
                    links = portfolio.query_links(skills)
                    email = llm.write_mail(job, links)
                    st.code(email, language='markdown')
            except Exception as e:
                st.error(f"An Error Occurred: {e}")
        else:
            st.warning("Please enter a valid URL and your name.")


if __name__ == "__main__":
    # Initialize the Chain and Portfolio
    chain = Chain()
    portfolio = Portfolio()

    # Configure Streamlit page
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")

    # Run the Streamlit app
    create_streamlit_app(chain, portfolio, clean_text)
