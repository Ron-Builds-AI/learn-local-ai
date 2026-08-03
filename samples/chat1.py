# GUIDE.md Part 5 -- your first client: one question, one answer, stdlib only.
import json
import urllib.request

OLLAMA = "http://127.0.0.1:11434"   # loopback: never leaves this PC
MODEL = "llama3.1:8b"

def ask(prompt):
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
    }
    req = urllib.request.Request(
        OLLAMA + "/api/chat",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=300) as resp:
        reply = json.loads(resp.read())
    return reply["message"]["content"]

print(ask("Explain what an API is in two sentences."))
