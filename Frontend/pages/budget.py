import customtkinter as ctk
import pyglet

budgetframe = None

def create(parent):
    global budgetframe
    budgetframe = ctk.CTkFrame(parent, fg_color="#937432")
    return budgetframe