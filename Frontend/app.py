import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import threading
import customtkinter as ctk
from Backend.Ai.ai import ask_ai

app = ctk.CTk()
app.title("Manager AI")
app.geometry("800x600")

chat_box = ctk.CTkTextbox(app, width=760, height=480, state="disabled")
chat_box.pack(pady=10)

bottom = ctk.CTkFrame(app)
bottom.pack(fill="x", padx=10, pady=5)

entry = ctk.CTkEntry(bottom, placeholder_text="Ask Manager anything...", width=620)
entry.pack(side="left", padx=5)

def send():
    prompt = entry.get()
    if not prompt:
        return
    
    chat_box.configure(state="normal")
    chat_box.insert("end", f"You: {prompt}\n\n")
    chat_box.configure(state="disabled")
    entry.delete(0, "end")
    
    entry.configure(state="disabled")
    button.configure(state="disabled")
    
    def get_response():
        response = ask_ai(prompt)
        chat_box.configure(state="normal")
        chat_box.insert("end", f"Manager: {response}\n\n")
        chat_box.configure(state="disabled")
        chat_box.see("end")
        entry.configure(state="normal")
        button.configure(state="normal")
    
    thread = threading.Thread(target=get_response)
    thread.start()

button = ctk.CTkButton(bottom, text="Send", command=send)
button.pack(side="left", padx=5)

app.mainloop()