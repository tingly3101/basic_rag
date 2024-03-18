import uuid
class Session():

    def __init__(self) -> None:
        self.session = {}
        
    def get_all_session(self):
        return self.session
    
    def start_session(self):
        new_session_id = str(uuid.uuid4())
        self.session[new_session_id] = {"history": []}
        return new_session_id, self.session[new_session_id]

    def check_session_id(self, session_id):
        if session_id in list(self.session.keys()):
            return True
        return False

    def get_history(self, session_id, n = 0 ) -> list:
        #return pair of history assistance and user
        if session_id not in list(self.session.keys()) or self.get_histiry_len(session_id) <= 0:
            return []
        #have history and session found
        if n == 0:
            return self.session[session_id]["history"]
        elif n >1:
            return self.session[session_id]["history"][-2*n:]


    
    def get_histiry_len(self, session_id):

        return len(self.session[session_id]["history"])
    
    def add_histories(self, messages: list[dict], session_id):
        self.session[session_id]["history"].extend(messages)

    def clear_history(self, session_id):
        self.session[session_id]["history"] = []
