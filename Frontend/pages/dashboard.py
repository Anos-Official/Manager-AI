import customtkinter as ctk
import pyglet

dashboardframe = None

def create(parent):
    global dashboardframe
    dashboardframe = ctk.CTkFrame(parent, fg_color="#784974")
    return dashboardframe