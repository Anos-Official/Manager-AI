import customtkinter as ctk
import pyglet

assitantframe = None

def create(parent):
    global assitantframe
    assitantframe = ctk.CTkFrame(parent, fg_color="#879808")
    return assitantframe