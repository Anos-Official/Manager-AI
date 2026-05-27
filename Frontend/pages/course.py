import customtkinter as ctk
import pyglet

courseframe = None

def create(parent):
    global courseframe
    courseframe = ctk.CTkFrame(parent, fg_color="#45815D")
    return courseframe