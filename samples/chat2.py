# GUIDE.md Part 6 -- a real conversation: the messages list IS the memory.
import json
import urllib.request

OLLAMA = "http://127.0.0.1:11434"
MODEL = "llama3.1:8b"

messages = [
    {"role": "system",
     "content": "You are a plain-spoken assistant. Short answers. No flattery."}
]

def call(messages):
    payload = {"model": MODEL, "messages": messages, "stream": False}
    req = urllib.request.Request(
        OLLAMA + "/api/chat",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=300) as resp:
        return json.loads(resp.read())["message"]

while True:
    user = input("you > ").strip()
    if user in ("/exit", ""):
        break
    messages.append({"role": "user", "content": user})
    msg = call(messages)
    messages.append(msg)                 # the model's reply joins the history
    print("ai  >", msg["content"])
