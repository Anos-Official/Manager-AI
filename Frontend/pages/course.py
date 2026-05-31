import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import threading
import re
import customtkinter as ctk
from Backend.Ai.ai import ask_ai

STUDY_SYSTEM_PROMPT = """You are a study guide advisor for Manager AI.
When given a career goal, recommend courses that specifically lead to that career.
When given a topic, recommend courses to master that topic.
Always include real free resources with working links to YouTube, Coursera, freeCodeCamp, Khan Academy, or similar free platforms.
Structure your response in exactly 3 phases: Beginner, Intermediate, Advanced.
For each phase list 3-5 specific courses with real links.
Format each course exactly like this:
- Course Name | URL | Platform"""

def create(parent):
    frame = ctk.CTkFrame(parent, fg_color="#323339", corner_radius=0)
    font = lambda size, bold=False: ctk.CTkFont(family="Nunito", size=size, weight="bold" if bold else "normal")

    ctk.CTkLabel(frame, text="Courses & Study Guide", font=font(26, bold=True)).pack(pady=(20,5))

    input_row = ctk.CTkFrame(frame, fg_color="transparent")
    input_row.pack(fill="x", padx=20, pady=10)

    goal_entry = ctk.CTkEntry(input_row, placeholder_text="What do you want to learn or become? (e.g. Python, Software Developer, Accountant)", font=font(14))
    goal_entry.pack(side="left", fill="x", expand=True, padx=(0,10))

    generate_btn = ctk.CTkButton(input_row, text="Generate", width=120, font=font(14, bold=True))
    generate_btn.pack(side="left")

    results_scroll = ctk.CTkScrollableFrame(frame, fg_color="#2C2D32", corner_radius=8)
    results_scroll.pack(fill="both", expand=True, padx=20, pady=10)

    ctk.CTkLabel(results_scroll, text="Your study guide will appear here.",
                 font=font(14), text_color="#888888").pack(pady=40)

    def generate():
        goal = goal_entry.get().strip()
        if not goal:
            return

        generate_btn.configure(state="disabled", text="Loading...")

        def run():
            prompt = f"""Create a complete study guide for someone who wants to: {goal}
If this is a career goal, recommend exactly what they need to study to get hired in Canada.
If this is a topic, recommend how to master it from beginner to advanced.
Structure into 3 phases: Beginner, Intermediate, Advanced.
For each phase list 3-5 free courses with real working links.
Format each course exactly like:
- Course Name | URL | Platform"""

            result = ask_ai(prompt, system_prompt=STUDY_SYSTEM_PROMPT)

            for w in results_scroll.winfo_children():
                w.destroy()

            for line in result.split("\n"):
                line = line.strip()
                if not line:
                    continue

                # phase headers
                if any(p in line.lower() for p in ["beginner", "intermediate", "advanced", "phase 1", "phase 2", "phase 3"]) and "http" not in line:
                    clean = re.sub(r'[#*]', '', line).strip()
                    if clean:
                        ctk.CTkLabel(results_scroll, text=clean,
                         font=font(16, bold=True)).pack(anchor="w", padx=15, pady=(15,5))

                # course lines
                elif "|" in line:
                    parts = line.lstrip("- ").split("|")
                    if len(parts) >= 2:
                        course_name = parts[0].strip()
                        link = parts[1].strip()
                        platform = parts[2].strip() if len(parts) > 2 else ""

                        row = ctk.CTkFrame(results_scroll, fg_color="transparent")
                        row.pack(fill="x", padx=15, pady=3)

                        var = ctk.BooleanVar()
                        cb = ctk.CTkCheckBox(row, text="", variable=var, width=20)
                        cb.pack(side="left")

                        ctk.CTkLabel(row, text=f"{course_name}  •  {platform}",
                                     font=font(13)).pack(side="left", padx=5)

                        link_btn = ctk.CTkButton(row, text="Open →", width=70,
                                                  font=font(12),
                                                  command=lambda l=link: __import__('webbrowser').open(l))
                        link_btn.pack(side="right", padx=5)

                # regular text lines
                else:
                    clean = re.sub(r'[#*+]', '', line).strip()
                    if clean:
                        ctk.CTkLabel(results_scroll, text=clean,
                                     font=font(13), wraplength=700,
                                     justify="left").pack(anchor="w", padx=15, pady=1)

            generate_btn.configure(state="normal", text="Generate")

        threading.Thread(target=run).start()

    generate_btn.configure(command=generate)

    return frame