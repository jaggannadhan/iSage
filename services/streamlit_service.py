import traceback
import streamlit as st
from services.email_service import send_email

def run_chat_assistant(query, choice_RAG, RAG_BAG):
    try:
        if query:
            # Display user query in chat message container
            st.chat_message("user").markdown(query)
            # Add user query to chat history
            st.session_state.messages.append({"role": "user", "content": query})

            with st.spinner("Thinking..."):
                try:
                    answer = RAG_BAG.get_answer(query, choice_RAG)
                except Exception:
                    print(traceback.format_exc())
                    answer = "Oops! I am unable to respond to your query, please try again later!"

            
            with st.chat_message("assistant"):
                st.markdown(answer)
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": answer})
    except Exception:
        print(traceback.format_exc())


def sidebar(model_types):
    with st.sidebar:
        
        st.header("🎓iSage - Immigrant Student Advisory Guidance Engine!" , divider="red")

        st.text("""ⓘ AI-powered legal guidance engine for Immgrant students in the U.S, providing trusted, up-to-date immigration from the official government sources (USCIS, educationusa, etc.). 
                """)
        
        st.divider()
        st.text("""  😎 Author: Jaggannadhan Venugopal""")
        st.page_link("https://www.linkedin.com/in/jvenu94/", label="Follow me on: Linkedin")
        st.page_link("https://www.github.com/jaggannadhan", label="Work with me on: GitHub")
        st.page_link("https://www.buymeacoffee.com/jaggannadhan", label="(or) Just Buy Me Protein 💪🏼")


        st.divider()
        if st.button("""🤩 We encourage your feedback!"""):
            feedback()
        else:
            show_feedback_response()
        
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