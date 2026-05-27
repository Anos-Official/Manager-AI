import customtkinter as ctk
import pyglet

careerframe = None

def create(parent):
    global careerframe
    careerframe = ctk.CTkFrame(parent, fg_color="#105975")
    return careerframe