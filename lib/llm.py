from openai import AzureOpenAI
from chatlib.session import Session
class LLM():

    def __init__(self, config: dict) -> None:
        self.openai_client = AzureOpenAI(
            api_key=config["llm"]["azure-open-ai"]["api-key"],
            api_version=config["llm"]["azure-open-ai"]["api-version"],
            azure_endpoint = config["llm"]["azure-open-ai"]["endpoint"]
        )
        self.model_name = config["llm"]["azure-open-ai"]["deployment-name"]
        # self.history = Session()

    def chat_completion(self, input_text: str=None, system_prompt: str=None):

        conversation = []
        if system_prompt and system_prompt != "":
            conversation.append({"role": "system", "content": system_prompt})
            
        if input_text and input_text != "":
            conversation.append({"role": "user", "content": input_text})
        # print(f"msg: {system_prompt}")
        response = self.openai_client.chat.completions.create(
            model=self.model_name,
            messages=conversation
        )
        # print(response)
        return response.choices[0].message.content
    
    def chat_completion_return_history(self,
                                       sess_id,
                                       session,
                                       input_text: str,
                                       system_prompt= ""):
        print("all_session", session.get_all_session())
        histories = session.get_history(session_id = sess_id, n = 2)
        
        conversation = []
        #first conversation
        
        if system_prompt and system_prompt != "":
            conversation.append({"role": "system", "content": system_prompt})
            
        if len(histories) > 0:
            conversation.extend(histories)      
        
        if input_text and input_text != "":
            conversation.append({"role": "user", "content": input_text})
            session.add_histories([{"role": "user", "content": input_text}], session_id=sess_id )

        
        # print(f"msg: {system_prompt}")
        response = self.openai_client.chat.completions.create(
            model=self.model_name,
            messages=conversation
        )
        session.add_histories([{"role": "assistant", "content": response.choices[0].message.content}], session_id=sess_id)

        
        return {"text": input_text, 
                "chat_completion": conversation,
                "response": response.choices[0].message.content, 
                "histories": session.get_history(session_id = sess_id)
        }




