import json, os
from openai import OpenAI

from langchain_openai import OpenAI as LangOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class LLMService:

    def __init__(self):
        self.user_session_id = "foo"
        self.OPENAI_CLIENT = OpenAI(
            api_key=OPENAI_API_KEY
        )
        self.LLM = LangOpenAI(
            openai_api_key=OPENAI_API_KEY,
            temperature=0.5
        )
        self.MemIns = {
            self.user_session_id: InMemoryChatMessageHistory()
        }

    def get_memory_ins(self, session_id):
        return self.MemIns.get(session_id)
    
    def create_chain(self, parser=StrOutputParser()):
        prompt_template = ChatPromptTemplate.from_messages(
            [MessagesPlaceholder(variable_name="history"), ("human",  f"{{question}}")]
        )

        chain = prompt_template | self.LLM | parser

        chain_with_history = RunnableWithMessageHistory(
            chain, 
            self.get_memory_ins,
            input_messages_key="question",
            history_messages_key="history"
        )
        return chain_with_history

    def send_completions_request(self, prompt):
        response = self.OPENAI_CLIENT.chat.completions.create(
            model="gpt-4",
            messages=prompt,
            max_tokens=3000
        )

        choices = response.choices[0]
        answer = choices.message.content
        # print(answer)
        return answer
    

    def answer_chain(self, context, question):
        prompt = """Answer the following question only based on the context provided. 
                    Answer if absolutely certain, else, say I don't know! Do not be verbose. 
                    Add sources (links) provided in the context.
                """ + f"Context: {context}\n\nQuestion: {question}"
        
        print(f"\n\nPrompt: {prompt}\n\n>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<")
        
        chain = self.create_chain()
        response = chain.invoke(
            { "question": prompt },
            config={"configurable": {"session_id": self.user_session_id}}
        )
        # print(response)
        return response
    
    def answer_based_on_context(self, context, question):
        prompt = [
            {
                "role": "system",
                "content": f"Answer the following question only based on the context provided. Answer if absolutely certain, else, say I don't know! Do not be verbose. Add sources (links) provided in the context"
            },
            {
                "role": "user",
                "content": f"Context: {context}\n\nQuestion: {question}"
            }
        ]

        print(f">>>>>>>>>>>>Context: {context}<<<<<<<<<<<<<<")
        answer = self.send_completions_request(prompt)
        return answer
        
    
    def clean_data_from_docs(self, data):
        sys_prompt = """Help me CLEAN the data from the raw text provided. 
        Exclude all headers, images and links and other unnecessary text like published dates, copyrights, Issue numbers etc., 
        I need all the relevant text from the document!
        Do not summarize, display as it is. Do not generate anything extra. Do not include data from other sources."""

        prompt = [
            {
                "role": "system",
                "content": sys_prompt
            },
            {
                "role": "user",
                "content": f"Raw Text: {data}"
            }
        ]

        answer = self.send_completions_request(prompt)
        return answer
