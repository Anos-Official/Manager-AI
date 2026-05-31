import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import customtkinter as ctk

def create(parent, switch_fns=None):
    frame = ctk.CTkFrame(parent, fg_color="#323339", corner_radius=0)
    font = lambda size, bold=False: ctk.CTkFont(family="Nunito", size=size, weight="bold" if bold else "normal")

    ctk.CTkLabel(frame, text="Welcome back, Mr. Scott",
                 font=font(28, bold=True)).pack(anchor="w", padx=30, pady=(30,5))
    ctk.CTkLabel(frame, text="Here's what you can do today.",
                 font=font(14), text_color="#888888").pack(anchor="w", padx=30, pady=(0,20))

    cards_frame = ctk.CTkFrame(frame, fg_color="transparent")
    cards_frame.pack(fill="x", padx=20)

    cards = [
        {
            "title": "Career Planner",
            "lines": [
                "What career do you want?",
                "Get a roadmap to get there",
                "See what skills you are missing",
            ],
            "key": "career"
        },
        {
            "title": "Budget Tracker",
            "lines": [
                "Add your income",
                "Track your expenses",
                "Let AI build your budget",
            ],
            "key": "budget"
        },
        {
            "title": "Tasks & Goals",
            "lines": [
                "Set goals and break them down",
                "Check off tasks as you go",
                "Get AI task suggestions",
            ],
            "key": "tasks"
        },
        {
            "title": "Study Guide",
            "lines": [
                "Type what you want to learn",
                "Get a beginner to advanced path",
                "Open free course links",
            ],
            "key": "study"
        }
    ]

    for card in cards:
        card_frame = ctk.CTkFrame(cards_frame, fg_color="#2C2D32", corner_radius=12, height=250)
        card_frame.pack(side="left", fill="both", expand=True, padx=8, pady=5)
        card_frame.pack_propagate(False)

        ctk.CTkLabel(card_frame, text=card["title"],
                     font=font(16, bold=True)).pack(pady=(20,10))

        for line in card["lines"]:
            ctk.CTkLabel(card_frame, text=f"- {line}", font=font(12),
                         text_color="#aaaaaa", wraplength=170,
                         justify="center").pack(pady=2)

        fn = switch_fns.get(card["key"]) if switch_fns else None
        ctk.CTkButton(card_frame, text="Open", font=font(12, bold=True),
                      fg_color="#1e6bb8", hover_color="#155a9a",
                      width=140, command=fn).pack(pady=20)

    ctk.CTkLabel(frame, text="Quick Tips", font=font(18, bold=True)).pack(anchor="w", padx=30, pady=(30,10))

    tips_frame = ctk.CTkFrame(frame, fg_color="#2C2D32", corner_radius=12)
    tips_frame.pack(fill="x", padx=20, pady=5)

    tips = [
        "Use the Career Planner to figure out exactly what you need to do to land your dream job.",
        "A simple rule for budgeting: 50% on needs, 30% on wants, 20% into savings.",
        "Big goals are easier when you break them into small daily tasks.",
        "30 minutes of learning every day adds up faster than you think.",
    ]

    for tip in tips:
        ctk.CTkLabel(tips_frame, text=tip, font=font(13),
                     text_color="#cccccc", wraplength=800,
                     justify="left", anchor="w").pack(anchor="w", padx=20, pady=6)

    return frame