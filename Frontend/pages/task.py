import customtkinter as ctk
import pyglet

taskframe = None

def create(parent):
    global taskframe
    taskframe = ctk.CTkFrame(parent, fg_color="#490878")
    return taskframe