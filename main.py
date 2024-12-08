import streamlit as st
from RAGModels import RAG_BAG

st.set_page_config(
    page_title="iSage",
    page_icon="./images/favico.png"
)

def sidebar(model_types):
    with st.sidebar:
        
        st.header("🎓iSage - Immigrant Student Advisory Guidance Engine!" , divider="red")

        st.text("""ⓘ AI-powered legal guidance engine for Immgrant students in the U.S, providing trusted, up-to-date immigration from the official government sources (USCIS, educationusa, etc.). 
                """)
        
        st.divider()
        st.text("""Author: Jaggannadhan Venugopal""")
        st.page_link("https://www.linkedin.com/in/jvenu94/", label="Follow me on: Linkedin")
        st.page_link("https://www.github.com/jaggannadhan", label="Work with me on: GitHub")
        st.page_link("https://www.buymeacoffee.com/jaggannadhan", label="(or) Just Buy Me Protein")


        st.divider()
        st.text("""Curiosity is a cat!
                Try different RAG model to compare performance!
                """)
        st.page_link("https://github.com/HKUDS/LightRAG", label="We recommend LightRAG for best performance", icon="⚡")
        toggle_RAG = st.sidebar.selectbox(
            "Select RAG Model",
            set(model_types),
            
        )

    return ( toggle_RAG )

def run_chat_assistant(query, choice_RAG, RAG_BAG):
    if query:
        # Display user query in chat message container
        st.chat_message("user").markdown(query)
        # Add user query to chat history
        st.session_state.messages.append({"role": "user", "content": query})

        with st.spinner("Thinking..."):
            answer = RAG_BAG.get_answer(query, choice_RAG)
        
        with st.chat_message("assistant"):
            st.markdown(answer)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": answer})


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