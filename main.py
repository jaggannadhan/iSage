import streamlit as st
from services.RAGModels import RAG_BAG
from services.streamlit_service import *

st.set_page_config(
    page_title="iSage",
    page_icon="./images/favico.png"
)

def iSage():
    choice_RAG = sidebar(RAG_BAG.model_types.keys())
    st.subheader("🎓iSage - Trusted Legal Guidance for Immigrant Students" , divider="red")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    query = st.chat_input("Ask me a question!")
    run_chat_assistant(query, choice_RAG, RAG_BAG)
    

if __name__ == "__main__":
    iSage()