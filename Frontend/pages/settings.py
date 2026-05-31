import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import customtkinter as ctk

def open_settings(app):
    font = lambda size, bold=False: ctk.CTkFont(family="Nunito", size=size, weight="bold" if bold else "normal")

    # settings panel
    panel = ctk.CTkFrame(app, fg_color="#2C2D32", corner_radius=12, width=700, height=500)
    panel.place(relx=0.5, rely=0.5, anchor="center")
    panel.pack_propagate(False)

    ctk.CTkLabel(panel, text="Settings", font=font(24, bold=True)).pack(pady=(30,10))
    ctk.CTkLabel(panel, text="This would be a settings page.",
                 font=font(16), text_color="#888888").pack(expand=True)

    def close(event=None):
        panel.destroy()

    # clicking the overlay closes it
    app.bind("<Button-1>", close)