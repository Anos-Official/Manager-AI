import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import threading
import customtkinter as ctk
from Backend.Ai.ai import ask_ai

ASSISTANT_SYSTEM_PROMPT = """You are Manager AI, a personal productivity assistant.
You help users with:
- Career planning and job market advice in Canada
- Budgeting and personal finance based on Canadian cost of living
- Task management and goal setting
- Course and study recommendations
Be conversational, helpful, and specific. Keep responses concise unless detail is needed."""

def create(parent):
    frame = ctk.CTkFrame(parent, fg_color="#323339", corner_radius=0)
    font = lambda size, bold=False: ctk.CTkFont(family="Nunito", size=size, weight="bold" if bold else "normal")

    conversation = []

    # chat area
    chat_scroll = ctk.CTkScrollableFrame(frame, fg_color="#323339")
    chat_scroll.pack(fill="both", expand=True, padx=15, pady=10)

    # input area
    input_border = ctk.CTkFrame(frame, fg_color="#2B2C31", height=70, corner_radius=0)
    input_border.pack(fill="x", side="bottom")
    input_border.pack_propagate(False)

    input_frame = ctk.CTkFrame(input_border, fg_color="#2C2D32", corner_radius=8)
    input_frame.pack(fill="both", expand=True, padx=10, pady=8)

    entry = ctk.CTkTextbox(input_frame, height=40, font=font(14), fg_color="transparent",
                            wrap="word")
    entry.pack(side="left", fill="both", expand=True, padx=10, pady=5)

    send_btn = ctk.CTkButton(input_frame, text="Send", width=80, font=font(13, bold=True))
    send_btn.pack(side="right", padx=10, pady=10)

    def add_bubble(text, is_user=True):
        bubble_frame = ctk.CTkFrame(chat_scroll, fg_color="transparent")
        bubble_frame.pack(fill="x", pady=4)

        bubble = ctk.CTkFrame(bubble_frame,
                               fg_color="#1e6bb8" if is_user else "#2C2D32",
                               corner_radius=12)

        label = ctk.CTkLabel(bubble, text=text, font=font(13),
                              wraplength=500, justify="left" if not is_user else "right")
        label.pack(padx=12, pady=8)

        if is_user:
            bubble.pack(side="right", padx=5)
        else:
            bubble.pack(side="left", padx=5)

        # scroll to bottom
        chat_scroll._parent_canvas.yview_moveto(1.0)

    def send():
        prompt = entry.get("1.0", "end").strip()
        if not prompt:
            return

        entry.delete("1.0", "end")
        send_btn.configure(state="disabled")

        add_bubble(prompt, is_user=True)
        conversation.append({"role": "user", "content": prompt})

        # loading indicator
        loading = ctk.CTkLabel(chat_scroll, text="Manager is typing...",
                                font=font(12), text_color="#888888")
        loading.pack(anchor="w", padx=20)
        chat_scroll._parent_canvas.yview_moveto(1.0)

        def run():
            response = ask_ai(prompt, system_prompt=ASSISTANT_SYSTEM_PROMPT)
            conversation.append({"role": "assistant", "content": response})
            loading.destroy()
            add_bubble(response, is_user=False)
            send_btn.configure(state="normal")

        threading.Thread(target=run).start()

    def on_enter(event):
        if event.state & 0x1:  # shift held
            entry.insert("end", "\n")
        else:
            send()
        return "break"

    entry.bind("<Return>", on_enter)
    send_btn.configure(command=send)

    # welcome message
    add_bubble("Hey! I'm Manager AI. I can help you with career planning, budgeting, tasks, and study recommendations. What's on your mind?", is_user=False)

    return frame