from PIL import Image as img
import customtkinter as ctk
import Frontend.pages.task as task
import Frontend.pages.dashboard as dash
import Frontend.pages.assistant as ass
import Frontend.pages.career as car
import Frontend.pages.course as cou
import Frontend.pages.profile as pro
import pyglet

toggled = False

#--window--
app = ctk.CTk()
app.title("Manager AI")
app.state("zoomed")
app.geometry("900x600")
app.iconbitmap("icon.ico")
app.configure(fg_color="#323339")

taskframe = task.create(app)
dashboardframe = dash.create(app)
assistantframe = ass.create(app)
careerframe = car.create(app)
courseframe = cou.create(app)
profileframe = pro.create(app)

#--Important Assets--
pyglet.font.add_file("Assets/Fonts/Nunito.ttf")

email = "123@gmailhtml.com"
User = "Mr. Scott"

icon = ctk.CTkImage(img.open("Assets/img/img icon.png"), size=(50,50))
sideclose = ctk.CTkImage(img.open("Assets/Icons/sidebar.png"), size=(30,30))
sideopen = ctk.CTkImage(img.open("Assets/Icons/sidebar2.png"), size=(30,30))
home = ctk.CTkImage(img.open("Assets/Icons/Home.png"), size=(30,30))
assist = ctk.CTkImage(img.open("Assets/Icons/Assist.png"), size=(30,30))
job = ctk.CTkImage(img.open("Assets/Icons/Job.png"), size=(30,30))
task_icon = ctk.CTkImage(img.open("Assets/Icons/tasks.png"), size=(30,30))
course = ctk.CTkImage(img.open("Assets/Icons/Course.png"), size=(30,30))
settings_icon = ctk.CTkImage(img.open("Assets/Icons/settings.png"), size=(30,30))
help_icon = ctk.CTkImage(img.open("Assets/Icons/help.png"), size=(30,30))
user_icon = ctk.CTkImage(img.open("Assets/Icons/user.png"), size=(50,50))

#--minibar--
minibar_border = ctk.CTkFrame(app, height=40, corner_radius=0, fg_color="#393A3F")
minibar_border.pack(side="top", fill="x")
minibar_border.pack_propagate(False)

minibar = ctk.CTkFrame(minibar_border, corner_radius=0, fg_color="#2B2C31")
minibar.pack(padx=0.6, pady=0.6, fill="both", expand=True)

#--sidebar--
sidebar_border = ctk.CTkFrame(app, width=250, fg_color="#393A3F")
sidebar_border.pack(side="left", fill="y")
sidebar_border.pack_propagate(False)

sidebar = ctk.CTkFrame(sidebar_border, corner_radius=1, fg_color="#2C2D32")
sidebar.pack(padx=0.6, pady=0.6, fill="both", expand=True)

#--functions--
def toggle_sidebar():
    global toggled
    if toggled:
        sidebar_border.configure(width=250)
        sidebar_btn.configure(image=sideclose)
        dashboard_btn.configure(text="Dashboard", width=270)
        assistant_btn.configure(text="Assistant", width=270)
        career_btn.configure(text="Career & Job Opportunities", width=270)
        task_btn.configure(text="Tasks & Goals", width=270)
        course_btn.configure(text="Courses & Study Guide", width=270)
        profile_btn.configure(text=f"{User}\n{email}", width=270)
        user_icon.configure(size=(50,50))
        toggled = False
    else:
        sidebar_border.configure(width=60)
        sidebar_btn.configure(image=sideopen)
        dashboard_btn.configure(text="", width=40)
        assistant_btn.configure(text="", width=40)
        career_btn.configure(text="", width=40)
        task_btn.configure(text="", width=40)
        course_btn.configure(text="", width=40)
        profile_btn.configure(text="", width=40)
        user_icon.configure(size=(40,40))
        toggled = True

def reset():
    dashboard_btn.configure(fg_color = "transparent")
    dashboardframe.pack_forget()
    assistant_btn.configure(fg_color = "transparent")
    assistantframe.pack_forget()
    career_btn.configure(fg_color = "transparent")
    careerframe.pack_forget()
    task_btn.configure(fg_color = "transparent")
    taskframe.pack_forget()
    course_btn.configure(fg_color = "transparent")
    courseframe.pack_forget()
    profile_btn.configure(fg_color = "transparent")
    profileframe.pack_forget()

def switchtotask():
    reset()
    task_btn.configure(fg_color="#121212")
    taskframe.pack(side = "right", fill="both", expand = "true")

def switchtodash():
    reset()
    dashboard_btn.configure(fg_color="#121212")
    dashboardframe.pack(side = "right", fill="both", expand = "true")


def switchtoass():
    reset()
    assistant_btn.configure(fg_color="#121212")
    assistantframe.pack(side = "right", fill="both", expand = "true")

def switchtocar():
    reset()
    career_btn.configure(fg_color="#121212")
    careerframe.pack(side = "right", fill="both", expand = "true")


def switchtocou():
    reset()
    course_btn.configure(fg_color="#121212")
    courseframe.pack(side = "right", fill="both", expand = "true")

def switchtopro():
    reset()
    profile_btn.configure(fg_color="#121212")
    profileframe.pack(side = "right", fill="both", expand = "true")


#--UI--
sidebar_btn = ctk.CTkButton(minibar, image=sideclose, text="", width=30, fg_color="transparent", hover_color="#121212", command=toggle_sidebar)
sidebar_btn.pack(side="left")

welcome_lbl = ctk.CTkLabel(minibar, image=icon, text=f"Welcome {User}", compound="left", font=ctk.CTkFont(family="Nunito", size=30, weight="bold"))
welcome_lbl.pack(side="left", expand=True)

settings_btn = ctk.CTkButton(minibar, image=settings_icon, text="", width=30, fg_color="transparent", hover_color="#121212")
settings_btn.pack(side="right")

help_btn = ctk.CTkButton(minibar, image=help_icon, text="", width=30, fg_color="transparent", hover_color="#121212")
help_btn.pack(side="right", padx=1)

dashboard_btn = ctk.CTkButton(sidebar, image=home, anchor="w", text="Dashboard", width=270, fg_color="transparent", hover_color="#121212", font=ctk.CTkFont(family="Nunito", size=16, weight="bold"), command=switchtodash)
dashboard_btn.pack(side="top", padx=4, pady=1)

assistant_btn = ctk.CTkButton(sidebar, image=assist, anchor="w", text="Assistant", width=270, fg_color="transparent", hover_color="#121212", font=ctk.CTkFont(family="Nunito", size=16, weight="bold"), command=switchtoass)
assistant_btn.pack(side="top", padx=4, pady=1)

career_btn = ctk.CTkButton(sidebar, image=job, anchor="w", text="Career & Job Opportunities", width=270, fg_color="transparent", hover_color="#121212", font=ctk.CTkFont(family="Nunito", size=15, weight="bold"), command=switchtocar)
career_btn.pack(side="top", padx=4, pady=1)

task_btn = ctk.CTkButton(sidebar, image=task_icon, anchor="w", text="Tasks & Goals", width=270, fg_color="transparent", hover_color="#121212", font=ctk.CTkFont(family="Nunito", size=16, weight="bold"), command=switchtotask)
task_btn.pack(side="top", padx=4, pady=1)

course_btn = ctk.CTkButton(sidebar, image=course, anchor="w", text="Courses & Study Guide", width=270, fg_color="transparent", hover_color="#121212", font=ctk.CTkFont(family="Nunito", size=16, weight="bold"), command=switchtocou)
course_btn.pack(side="top", padx=4, pady=1)

#--profile--
profile_border = ctk.CTkFrame(sidebar, width=250, height=70, fg_color="#393A3F")
profile_border.pack(side="bottom")
profile_border.pack_propagate(False)

profile_btn = ctk.CTkButton(profile_border, anchor="w", image=user_icon, text=f"{User}\n{email}", width=270, height=67, fg_color="#2C2D32", hover_color="#121212", font=ctk.CTkFont(family="Nunito", size=16, weight="bold"), command=switchtopro)
profile_btn.pack(side="left")

dashboardframe.pack(side = "right", fill = "both", expand = "true")
app.mainloop()