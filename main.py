from fastapi import FastAPI, HTTPException
from chatlib.session import Session
from lib.chain import ConversationChain
from lib.utils import load_config_yaml
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--config', required=True, type=str, help="YAML config file")      # option that takes a value

args = parser.parse_args()
config = load_config_yaml(args.config)
app = FastAPI()
sess = Session()





@app.get("/")
def default():
    return "LLM Service is running"
#create session
@app.post("/sessions")
def create_session():
    try:
        session_id, history = sess.start_session()
        return {"status": "succeed", "session_id": session_id, "history": history["history"]}
    except:
        raise HTTPException(status_code=500, detail="Create session Failed")
#get all session
@app.get("/sessions")
def get_all_session():
    try:
        all_session = sess.get_all_session()
        return {"status": "succeed", "sessions": all_session}
    except:
        raise HTTPException(status_code=500, detail="Cannot get session.")
    
@app.get("/sessions/{session_id}")
def get_sessions(session_id):
    if not sess.check_session_id(session_id):
        raise HTTPException(status_code=400, detail="Session not found.")
    history = sess.get_history(session_id)
    return {"status": "succeed", "detail":"session_found", "session_id": session_id, "histories": history}


@app.get("/chat_completion/{session_id}")
def chat_completion(session_id, text_input: str):
    #check session_is exist?
    if not sess.check_session_id(session_id):
        raise HTTPException(status_code=400, detail="Session not found.")
    #create conversation instance
    conversation_chain = ConversationChain(config)
    answer = conversation_chain.rag_chain_include_history(session_id, sess, text_input)

    return answer



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", reload=True)