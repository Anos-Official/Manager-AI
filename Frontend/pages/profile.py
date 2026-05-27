import customtkinter as ctk
import pyglet

profileframe = None

def create(parent):
    global profileframe
    profileframe = ctk.CTkFrame(parent, fg_color="#948339")
    return profileframe