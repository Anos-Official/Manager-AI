from PIL import Image as img
import customtkinter as ctk
import pyglet

toggled = False



#--window--
app = ctk.CTk()
app.title("Manager AI")
app.geometry("900x600")
app.iconbitmap("icon.ico")
app.configure(fg_color="#323339")



#--Important Assets and stuff--
pyglet.font.add_file("Assets/Fonts/Nunito.ttf")


sideclose = ctk.CTkImage(img.open("Assets/Icons/sidebar.png"), size=(30,30))
sideopen = ctk.CTkImage(img.open("Assets/Icons/sidebar2.png"), size=(30,30))
home = ctk.CTkImage(img.open("Assets/Icons/Home.png"), size=(30,30))
assist = ctk.CTkImage(img.open("Assets/Icons/Assist.png"), size=(30,30))
job = ctk.CTkImage(img.open("Assets/Icons/Job.png"), size=(30,30))
task = ctk.CTkImage(img.open("Assets/Icons/tasks.png"), size=(30,30))
course = ctk.CTkImage(img.open("Assets/Icons/Course.png"), size=(30,30))
settings = ctk.CTkImage(img.open("Assets/Icons/settings.png"), size=(30,30))
helpicon = ctk.CTkImage(img.open("Assets/Icons/help.png"), size=(30,30))





#--small minibar--
minibarborder = ctk.CTkFrame(app, height= 40, corner_radius=0, fg_color="#393A3F")
minibarborder.pack(side="top", fill = "x")
minibarborder.pack_propagate(False)

minibar = ctk.CTkFrame(minibarborder, corner_radius=0, fg_color="#2B2C31")
minibar.pack(padx = 0.6, pady = 0.6, fill = "both", expand = True)

#--sidebar--
sidebarborder = ctk.CTkFrame(app, width= 250, fg_color="#393A3F")
sidebarborder.pack(side="left", fill ="y")
sidebarborder.pack_propagate(False)

sidebar = ctk.CTkFrame(sidebarborder, corner_radius = 1, fg_color="#2C2D32")
sidebar.pack(padx = 0.6, pady = 0.6, fill = "both", expand = True)


#--functions--
def toggle_sidebar():
    global toggled
    if toggled:
        sidebarborder.configure(width=250)
        sidebarbtn.configure(image=sideclose)
        dashboardbtn.configure(text="Dashboard", width=270)
        Assistantbtn.configure(text="Assistant", width=270)
        Careerbtn.configure(text="Career & Job Opportunities", width=270)
        Taskbtn.configure(text="Tasks & Goals", width=270)
        Coursebtn.configure(text="Courses & Study Guide", width=270)
        toggled = False
    else:
        sidebarborder.configure(width=60)
        sidebarbtn.configure(image=sideopen)
        dashboardbtn.configure(text="", width=40)
        Assistantbtn.configure(text="", width=40)
        Careerbtn.configure(text="", width=40)
        Taskbtn.configure(text="", width=40)
        Coursebtn.configure(text="", width=40)
        toggled = True



#--buttons--
sidebarbtn = ctk.CTkButton(minibar, image=sideclose, text="", width = 30, fg_color="transparent", hover_color="#121212", command=toggle_sidebar)
sidebarbtn.pack(side="left")

settingsbtn = ctk.CTkButton(minibar, image=settings, text="", width = 30, fg_color="transparent", hover_color="#121212")
settingsbtn.pack(side="right")

helpbtn = ctk.CTkButton(minibar, image=helpicon, text="", width = 30, fg_color="transparent", hover_color="#121212")
helpbtn.pack(side="right", padx = 1)

dashboardbtn = ctk.CTkButton(sidebar, image=home, anchor="w", text="Dashboard", width=270,fg_color="transparent", hover_color="#121212", font=ctk.CTkFont(family="Nunito", size = 16, weight = "bold"))
dashboardbtn.pack(side="top",padx = 4, pady= 1)

Assistantbtn = ctk.CTkButton(sidebar, image=assist, anchor="w", text="Assistant", width=270,fg_color="transparent", hover_color="#121212", font=ctk.CTkFont(family="Nunito", size = 16, weight = "bold"))
Assistantbtn.pack(side="top",padx = 4, pady= 1)

Careerbtn = ctk.CTkButton(sidebar, image=job, anchor="w", text="Career & Job Opportunites", width=270,fg_color="transparent", hover_color="#121212", font=ctk.CTkFont(family="Nunito", size = 16, weight = "bold"))
Careerbtn.pack(side="top",padx = 4, pady= 1)

Taskbtn = ctk.CTkButton(sidebar, image=task, anchor="w", text="Tasks & Goals", width=270,fg_color="transparent", hover_color="#121212", font=ctk.CTkFont(family="Nunito", size = 16, weight = "bold"))
Taskbtn.pack(side="top",padx = 4, pady= 1)

Coursebtn = ctk.CTkButton(sidebar, image=course, anchor="w", text="Courses & Study Guide", width=270,fg_color="transparent", hover_color="#121212", font=ctk.CTkFont(family="Nunito", size = 16, weight = "bold"))
Coursebtn.pack(side="top",padx = 4, pady= 1)


app.mainloop()