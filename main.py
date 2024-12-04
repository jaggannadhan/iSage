import streamlit as st
from ai21.models.chat import ChatMessage
from retriever import *
from load_RAG import LoadRAG


def main(rag_model):
    st.set_page_config(page_title="iSAGE")
    st.header("iSAGE")
    st.subheader("- Immigrant Student Advisory Guidance Engine!" , divider="red")

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

        top_chunks = retrieve_top_k_chunks(
            query, 
            rag_model.embedding_model, 
            rag_model.index, 
            rag_model.chunks, 
            k=5
        )
        answer = generate_answer(query, top_chunks)
        with st.chat_message("assistant"):
            st.markdown(answer)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": answer})


if __name__ == "__main__":
    rag_model = LoadRAG()
    main(rag_model)