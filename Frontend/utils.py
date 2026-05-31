import tkinter.font as tkfont

def render_markdown(textbox, text):
    textbox.configure(state="normal")
    textbox.delete("1.0", "end")

    # ✅ Access the underlying tk.Text widget to use font in tag_config
    tk_text = textbox._textbox

    tk_text.tag_config("h1",     font=tkfont.Font(family="Nunito", size=20, weight="bold"))
    tk_text.tag_config("h2",     font=tkfont.Font(family="Nunito", size=16, weight="bold"))
    tk_text.tag_config("bold",   font=tkfont.Font(family="Nunito", size=13, weight="bold"))
    tk_text.tag_config("normal", font=tkfont.Font(family="Nunito", size=13))

    for line in text.split("\n"):
        if line.startswith("## "):
            tk_text.insert("end", line[3:] + "\n", "h2")
        elif line.startswith("# "):
            tk_text.insert("end", line[2:] + "\n", "h1")
        elif line.startswith("- ") or line.startswith("* "):
            tk_text.insert("end", "  • " + line[2:] + "\n", "normal")
        elif line.startswith("**") and line.endswith("**"):
            tk_text.insert("end", line[2:-2] + "\n", "bold")
        else:
            tk_text.insert("end", line + "\n", "normal")

    textbox.configure(state="disabled")