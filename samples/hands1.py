# GUIDE.md Part 9 -- one read-only hand, a jail, and the dispatcher that IS the
# security boundary. The model proposes; this code disposes.
import json
import os
import urllib.request

OLLAMA = "http://127.0.0.1:11434"
MODEL = "llama3.1:8b"
JAIL = os.path.realpath(r"C:\learn_ai\sandbox")   # the ONE folder hands may touch

TOOLS = [{
    "type": "function",
    "function": {
        "name": "list_folder",
        "description": "List the files in a folder inside the working area.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string",
                         "description": "Folder path to list"}},
            "required": ["path"],
        },
    },
}]

def run_hand(name, args):
    """The dispatcher. THE security boundary. The model never gets past here."""
    if name != "list_folder":
        return "REFUSED: no such hand."
    target = os.path.realpath(str(args.get("path", "")))  # resolves .. and links
    if not target.startswith(JAIL):                       # the jail check
        return "REFUSED: that path is outside the working folder."
    try:
        return "\n".join(sorted(os.listdir(target))) or "(empty)"
    except OSError as e:
        return "ERROR: %s" % e

def call(messages):
    payload = {"model": MODEL, "messages": messages,
               "tools": TOOLS, "stream": False}
    req = urllib.request.Request(
        OLLAMA + "/api/chat",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=300) as resp:
        return json.loads(resp.read())["message"]

os.makedirs(JAIL, exist_ok=True)
messages = [{"role": "system", "content":
             "You have a list_folder tool for the working folder. "
             "Use it rather than guessing what files exist."}]

while True:
    user = input("you > ").strip()
    if user in ("/exit", ""):
        break
    messages.append({"role": "user", "content": user})
    while True:                                   # loop: model may chain tools
        msg = call(messages)
        messages.append(msg)
        calls = msg.get("tool_calls")
        if not calls:
            print("ai  >", msg["content"])
            break
        for tc in calls:
            fn = tc["function"]
            print("[hand] %s(%s)" % (fn["name"], fn["arguments"]))
            result = run_hand(fn["name"], fn["arguments"])
            messages.append({"role": "tool", "content": result})
