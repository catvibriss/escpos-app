import customtkinter as ctk
import tkinter as tk

from .objects import Page
 
class Content(Page):
    def __init__(self, master, name: str, printer, *args, **kwargs):
        super().__init__(master=master, name=name, printer=printer, *args, **kwargs)