import os
from dotenv import load_dotenv
import streamlit as st
from RAGModels import RAG_BAG

load_dotenv()


def get_answer(query, choice_RAG):
    rag_model = RAG_BAG.get_model(model=choice_RAG)

    if(choice_RAG == "LightRAG"):
        answer = rag_model.generate_answer(query)
        return answer

    top_chunks = rag_model.retrieve_top_k_chunks(query, k=5)
    answer = rag_model.generate_answer(query, top_chunks)

    return answer

def sidebar(model_types):
    with st.sidebar:
        st.title("🎓iSage")
        st.subheader(" - Immigrant Student Advisory Guidance Engine!" , divider="red")
        toggle_RAG = st.sidebar.selectbox(
            "Select RAG Model",
            set(model_types)
        )

    return ( toggle_RAG )

def main():
    st.set_page_config(page_title="iSAGE")
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
    

    if query:
        # Display user query in chat message container
        st.chat_message("user").markdown(query)
        # Add user query to chat history
        st.session_state.messages.append({"role": "user", "content": query})

        with st.spinner("Thinking..."):
            answer = get_answer(query, choice_RAG)
        
        with st.chat_message("assistant"):
            st.markdown(answer)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": answer})


if __name__ == "__main__":
    main()