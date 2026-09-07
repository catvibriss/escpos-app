import customtkinter as ctk
import tkinter as tk

from gui.objects import Page

class Content(Page):
    def __init__(self, *args, **kwargs):
        super().__init__(name="printer", *args, **kwargs)
