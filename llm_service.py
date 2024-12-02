import json
from openai import OpenAI

OPENAI_CLIENT = OpenAI(api_key='sk-hBSd8x6rxdExfV1iP-77MJO9cXIKicCs9q_4nwAYxWT3BlbkFJTM8Te0qgeNMQsO-BmLNGFt4CQ5kMUq1AP_5YcX3NMA')

class OpenAIService:
    def send_completions_request(self, prompt):
        response = OPENAI_CLIENT.chat.completions.create(
            model="gpt-4",
            messages=prompt,
            max_tokens=1000
        )

        choices = response.choices[0]
        answer = choices.message.content
        print(answer)
        return answer
    
    def answer_based_on_context(self, context, question):
        prompt = [
            {
                "role": "system",
                "content": f"Answer the following question only based on the context provided. Answer if absolutely certain, else, say you don't know! Do not be verbose."
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
