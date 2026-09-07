import customtkinter as ctk
import tkinter as tk

from gui import sidebar
from gui.pages import PAGES
from gui.manager import AppManager

from escpos.printer import SerialPrinter

def _test_monitor(data, dtype):
    print(dtype, data.hex(" "))

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # setup
        self.main_printer = SerialPrinter(serial_handler=_test_monitor)
        self.manager = AppManager(self.main_printer)

        self.title("esc/pos printer app")
        self.minsize(1200, 700)
        self.geometry("1200x700")

        self.configure(fg_color="#181818")

        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True)

        # sidebar
        sidebar_frame = ctk.CTkFrame(container, width=240, corner_radius=0)
        sidebar_frame.pack(side="left", fill="y")
        sidebar_frame.pack_propagate(False)

        self.master_sidebar = sidebar.Sidebar(sidebar_frame, self.manager)
        self.master_sidebar.pack(padx=0, pady=0, fill="both", expand=True)

        # content
        content_container = ctk.CTkFrame(container, fg_color="transparent")
        content_container.pack(side="left", fill="both", expand=True)

        # topbar
        self.topbar = ctk.CTkFrame(content_container, height=30, corner_radius=0,
            fg_color="transparent")
        self.topbar.pack(side="top", fill="x", padx=(8, 0))
        self.topbar.pack_propagate(False)

        # pages
        self.content_frame = ctk.CTkScrollableFrame(content_container, corner_radius=0,
            fg_color="#181818", scrollbar_button_color="#222222", scrollbar_button_hover_color="#333333")
        self.content_frame.pack(side="top", fill="both", expand=True)

        self.pages = {}

        pages = PAGES

        for page_class in pages:
            page = page_class(master=self.content_frame, manager=self.manager)

            self.pages[page.name] = page

            button = ctk.CTkButton(self.topbar, text=page.name, width=0, height=32,
                corner_radius=6, fg_color="transparent", hover_color="#222222",
                text_color="#aaaaaa", font=ctk.CTkFont(size=13),
                command=lambda name=page.name: self.show_page(name))
            button.pack(side="left", padx=(0, 4))

        if self.pages:
            self.show_page(next(iter(self.pages)))

    def show_page(self, name: str):
        for page in self.pages.values():
            page.pack_forget()

        page = self.pages[name]
        page.pack(side="top", fill="both", padx=16)