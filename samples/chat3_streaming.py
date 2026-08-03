# GUIDE.md Part 7 -- same conversation loop, but the reply streams in live.
import json
import urllib.request

OLLAMA = "http://127.0.0.1:11434"
MODEL = "llama3.1:8b"

messages = [
    {"role": "system",
     "content": "You are a plain-spoken assistant. Short answers. No flattery."}
]

def call_streaming(messages):
    payload = {"model": MODEL, "messages": messages, "stream": True}
    req = urllib.request.Request(
        OLLAMA + "/api/chat",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    content = ""
    with urllib.request.urlopen(req, timeout=300) as resp:
        for raw_line in resp:                      # HTTP body, line by line
            chunk = json.loads(raw_line)
            piece = chunk.get("message", {}).get("content", "")
            print(piece, end="", flush=True)       # print as it arrives
            content += piece
            if chunk.get("done"):
                break
    print()
    return {"role": "assistant", "content": content}

while True:
    user = input("you > ").strip()
    if user in ("/exit", ""):
        break
    messages.append({"role": "user", "content": user})
    print("ai  > ", end="", flush=True)
    messages.append(call_streaming(messages))
