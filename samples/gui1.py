# GUIDE.md Part 10 -- minimal windowed chat. Worker thread talks to the model,
# a queue crosses to the GUI thread, after() polls it. The window never blocks.
import json
import queue
import threading
import tkinter as tk
import urllib.request
from tkinter import scrolledtext

OLLAMA = "http://127.0.0.1:11434"
MODEL = "llama3.1:8b"
Q = queue.Queue()
messages = [{"role": "system", "content": "Short, plain answers."}]

def worker(user_text):
    messages.append({"role": "user", "content": user_text})
    payload = {"model": MODEL, "messages": messages, "stream": True}
    req = urllib.request.Request(
        OLLAMA + "/api/chat",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"})
    content = ""
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            for line in resp:
                chunk = json.loads(line)
                piece = chunk.get("message", {}).get("content", "")
                content += piece
                Q.put(piece)                     # -> the GUI thread
                if chunk.get("done"):
                    break
        messages.append({"role": "assistant", "content": content})
    except OSError as e:
        Q.put("\n[error talking to Ollama: %s]" % e)
    Q.put("\n\n")

win = tk.Tk()
win.title("my first ai window")
txt = scrolledtext.ScrolledText(win, wrap="word", state="disabled")
txt.pack(fill="both", expand=True)
entry = tk.Entry(win)
entry.pack(fill="x")

def append(s):
    txt.configure(state="normal")
    txt.insert("end", s)
    txt.see("end")
    txt.configure(state="disabled")

def on_send(_event=None):
    user = entry.get().strip()
    if not user:
        return
    entry.delete(0, "end")
    append("you > %s\nai  > " % user)
    threading.Thread(target=worker, args=(user,), daemon=True).start()

def poll():
    try:
        while True:
            append(Q.get_nowait())
    except queue.Empty:
        pass
    win.after(50, poll)                          # re-arm the poll

entry.bind("<Return>", on_send)
win.after(50, poll)
entry.focus_set()
win.mainloop()
