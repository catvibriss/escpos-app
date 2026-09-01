import customtkinter as ctk
import tkinter as tk

from escpos.printer import SerialPrinter

class Page(ctk.CTkFrame):
    def __init__(self, master, name: str, printer: SerialPrinter, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.printer = printer
        self.name = name
