import traceback
import streamlit as st
import pandas as pd
from services.email_service import send_email


def chat_window(choice_RAG, RAG_BAG):
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    message_container = st.container(height=550, border=False)

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with message_container.chat_message(message["role"]):
            message_container.markdown(message["content"])

    if query := st.chat_input("Ask me a question!"):
        run_chat_assistant(query, choice_RAG, RAG_BAG, message_container)


def run_chat_assistant(query, choice_RAG, RAG_BAG, message_container):
    try:
        # Display user query in chat message container
        message_container.chat_message("user").markdown(query)
        # Add user query to chat history
        st.session_state.messages.append({"role": "user", "content": query})

        with message_container:
            with st.spinner("Thinking..."):
                try:
                    answer = RAG_BAG.get_answer(
                        query=query, 
                        choice_RAG=choice_RAG
                    )
                except Exception:
                    print(traceback.format_exc())
                    answer = "Oops! I am unable to respond to your query, please try again later!"

        
        with message_container.chat_message("assistant"):
            message_container.markdown(answer)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": answer})
    except Exception:
        print(traceback.format_exc())


def sidebar(model_types):
    with st.sidebar:
        
        st.header("🎓iSage - Immigrant Society Advisory Guidance Engine!" , divider="red")

        st.text("""ⓘ AI-powered legal guidance engine for Immigrants in the U.S, providing trusted, up-to-date immigration from the official government sources (USCIS, educationusa, etc.). 
                """)
        
        if st.button("🤔 How to use?"):
            how_to()
        
        if st.button("""🤩 We encourage your feedback!"""):
            feedback()
        else:
            show_feedback_response()

        st.divider()

        st.text("""  😎 Author: Jaggannadhan Venugopal""")
        st.page_link("https://www.linkedin.com/in/jvenu94/", label="Follow me on: Linkedin")
        st.page_link("https://www.github.com/jaggannadhan", label="Work with me on: GitHub")
        st.page_link("https://www.buymeacoffee.com/jaggannadhan", label="(or) Just Buy Me Protein 💪🏼")

        st.divider()

        st.text("""😼 Curiosity is a cat!
                Try different RAG models to compare performance!
                """)
        st.page_link("https://github.com/HKUDS/LightRAG", label="We recommend LightRAG for best performance", icon="⚡")
        toggle_RAG = st.sidebar.segmented_control(
            "Select RAG Model",
            set(model_types),
            default="LightRAG"
        )
        
    return ( toggle_RAG )


@st.dialog("Give us your Feedback!")
def feedback():
    st.write("Liked iSage? What can we improve on? Let us know!")
    your_email = st.text_input("Your Email")
    subject = st.text_input("Subject")
    message = st.text_area("Message")
    if st.button("Submit"):
        success, reason = send_email(your_email, subject, message)            
        if not ("cannot be empty" in reason):
            st.session_state.feedback = {"success": success, "reason": reason}    
            st.rerun()
        
        
def show_feedback_response():
    try:
        if "feedback" in st.session_state: 
            email_resp = st.session_state.feedback
            resp_status = email_resp.get("success")
            if resp_status:
                st.balloons()
                st.toast("Feedback submitted!", icon="✅")
            else:
                st.toast("Unable to submit feedback, pls try later!", icon="❌")
            st.session_state.pop("feedback")
    except Exception:
        print(traceback.format_exc())


@st.dialog("🤔 How to use?")
def how_to():
    st.write("""1) iSage is engineered to serve brief responses due to token limits. Future updates to the app will provide detailed responses and links to forms.""")
    st.write("""2) Kindly use the feedback feature to submit your queries/concerns to me. I will take up most raised bugs during my weekends to work on.""")
    st.write("""3) I use a hashmap-based caching setup to address repeated questions. So feel free to ask the same questions again if your session is lost or if you need to refresh your memory. But for new questions please try to keep it to less than 5 questions per session.""")
    st.write("""4) Please refrain from using profanity. We understand that student life can be frustrating, foul language will not make it better.""")
    

def show_FAQ_table(FAQ):
    try:
        if not FAQ:
            print("No FAQs")
            return
        questions = list(FAQ.keys())
        columns = {
            "questions": questions,
            "votes": []
        }

        for question in questions:
            entity = FAQ.get(question)
            votes = entity.get("votes")
            columns["votes"].append(votes)

        data_df = pd.DataFrame(columns)

        st.data_editor(
            data_df,
            column_config={
                "questions": st.column_config.TextColumn(
                    "Questions",
                    disabled=True,
                    width="large"
                ),
                "votes": st.column_config.NumberColumn(
                    "Votes",
                    disabled=True,
                    width="small"
                ),
            },
            height=600,
            width=1000,
            hide_index=True,
        )
    except Exception:
        print("Error in show_FAQ_table")
        print(traceback.format_exc())