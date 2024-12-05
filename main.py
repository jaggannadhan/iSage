import os
import streamlit as st
from retriever import RAGOps
from load_RAG import LoadRAG


def main():
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

        top_chunks = rag_ops.retrieve_top_k_chunks(
            query, 
            rag_model.embedding_model, 
            rag_model.index, 
            rag_model.chunks, 
            k=5
        )
        answer = rag_ops.generate_answer(query, top_chunks)
        with st.chat_message("assistant"):
            st.markdown(answer)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": answer})


rag_ops = RAGOps()
rag_model = LoadRAG()

if __name__ == "__main__":
    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    main()