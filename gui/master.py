import customtkinter as ctk
import tkinter as tk

from gui import sidebar, settings
from .manager import AppManager

from escpos.printer import SerialPrinter

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # setup
        self.main_printer = SerialPrinter()
        self.manager = AppManager(self.main_printer)

        self.title("esc/pos printer app")
        self.minsize(1200, 700)
        self.geometry("1200x700")

        self.configure(fg_color="#111111")

        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True)

        # sidebar
        sidebar_frame = ctk.CTkFrame(container, width=240, corner_radius=0)
        sidebar_frame.pack(side="left", fill="y")
        sidebar_frame.pack_propagate(False)

        self.master_sidebar = sidebar.Sidebar(sidebar_frame, self.manager)
        self.master_sidebar.pack(padx=0, pady=0, fill="both", expand=True)

        # content
        self.content_frame = ctk.CTkScrollableFrame(container, corner_radius=0, fg_color="#181818",
            scrollbar_button_color="#222222", scrollbar_button_hover_color="#333333")
        self.content_frame.pack(side="left", fill="both", expand=True)

        # TODO: pagination
        test_page = settings.Content(master=self.content_frame, manager=self.manager)
        test_page.pack(side="top", fill="both")

ctk.set_appearance_mode("dark")