import streamlit as st
from services.RAGModels import RAG_BAG
from services.cache_service import CloudCacheService
from services.streamlit_service import *
from static.main_css import main_css


def get_FAQ():
    RAG_BAG.cache_service = CloudCacheService()
    FAQ = RAG_BAG.cache_service.get_top_queries(k=50)
    return FAQ


def main():
    st.set_page_config(
        page_title="iSage",
        page_icon="./images/favico.png",
        layout="wide"
    )

    st.markdown(
        main_css,
        unsafe_allow_html=True,
    )

    with st.spinner("Getting FAQ"):
        FAQ = get_FAQ()

    tab1, tab2 = st.tabs(["Assistant", "FAQ"])    
    choice_RAG = sidebar(RAG_BAG.model_types.keys())
    
    with tab1:
        st.subheader("🎓iSage - Trusted Legal Guidance for Immigrant Society" , divider="red")
        chat_window(choice_RAG, RAG_BAG)
    
    with tab2:
        st.subheader("FAQ Section", divider="red")
        show_FAQ_table(FAQ)


if __name__ == "__main__":
    main()