import streamlit as st
from prreviewer import PrReviewer
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Test")

st.header("Code Reviewer")

# Initialize session state for chat history if it doesn't exist
# if 'chat_history' not in st.session_state:
#     st.session_state['chat_history'] = []


gitDff = st.text_input("Enter git diff:")
jiraId = st.text_input("Enter jiraId:")

# # User input fields
# departure_city = st.text_input("Origin City:")
# destination_city = st.text_input("Destination City:")
# departure_date = st.date_input("Departure Date:")
# adults_count = st.number_input("Number of Adults:", min_value=1, step=1)
# child_count = st.number_input("Number of Children:", min_value=0, step=1)
# infant_count = st.number_input("Number of Infants:", min_value=0, step=1)

submit = st.button("Ask")

if submit and gitDff or submit and jiraId:

    # Process the natural language input to extract flight details
    prReviewer = PrReviewer()
    result = prReviewer.run(gitDff)
    st.write(result)