import streamlit as st
from services.RAGModels import LOAD_RAG_MODEL
from services.cache_service import CloudCacheService
from services.streamlit_service import *

st.set_page_config(
    page_title="iSage",
    page_icon="./images/favico.png",
    layout="wide"
)

tab1, tab2 = st.tabs(["Assistant", "FAQ"])
    
@st.cache_resource()
def get_rag_models():
    RAG_BAG = LOAD_RAG_MODEL()
    return RAG_BAG

def get_FAQ(_cache_service):
    FAQ = _cache_service.get_top_queries(k=50)
    return FAQ

def iSage():
    RAG_BAG = get_rag_models()

    with st.spinner("Getting FAQ"):
        RAG_BAG.cache_service = CloudCacheService()
        FAQ = get_FAQ(RAG_BAG.cache_service)
    
    choice_RAG = sidebar(RAG_BAG.model_types.keys())
    
    with tab1:
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
    
    
    with tab2:
        st.subheader("FAQ Section", divider="red")
        if FAQ:
            show_FAQ_table(FAQ)

# st.cache_resource.clear()

if __name__ == "__main__":
    iSage()