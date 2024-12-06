import os
import streamlit as st
from load_RAG import RAG_MOD_BASIC, RAG_MOD_SKLEARN


def sidebar():
    with st.sidebar:
        st.title("🎓iSage")
        st.subheader(" - Immigrant Student Advisory Guidance Engine!" , divider="red")
        toggle_RAG = st.sidebar.selectbox(
            "Select RAG Model",
            ("FAISS", "SKLearn")
        )

    return ( toggle_RAG )

def main():
    st.set_page_config(page_title="iSAGE")
    choice_RAG = sidebar()

    st.subheader("🎓iSage - Trusted Legal Guidance for Immigrant Students" , divider="red")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    query = st.chat_input("Ask me a question!")
    rag_model_types = {
        "FAISS": rag_faiss,
        "SKLearn": rag_sklearn
    }
    rag_model = rag_model_types.get(choice_RAG)

    if query:
        # Display user query in chat message container
        st.chat_message("user").markdown(query)
        # Add user query to chat history
        st.session_state.messages.append({"role": "user", "content": query})

        top_chunks = rag_model.retrieve_top_k_chunks(query, k=5)
        answer = rag_model.generate_answer(query, top_chunks)
        with st.chat_message("assistant"):
            st.markdown(answer)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": answer})


rag_faiss = RAG_MOD_BASIC()
rag_sklearn = RAG_MOD_SKLEARN()

if __name__ == "__main__":
    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    main()