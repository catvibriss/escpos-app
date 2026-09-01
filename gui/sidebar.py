import customtkinter as ctk
import tkinter as tk

from escpos.printer import SerialPrinter
from escpos.profile import Profile

import serial
import serial.tools.list_ports

def fetch_ports():
    ports = serial.tools.list_ports.comports()
    formatted_ports = []

    for port in ports:
        device = port.device
        description = port.description

        if not description or description == device:
            description = "unidentified"

        formatted_ports.append(f"{device} | {description}")

    return formatted_ports
         
class Sidebar(ctk.CTkFrame):
    def __init__(self, parent, printer: SerialPrinter, *args, **kwargs):
        super().__init__(master=parent, width=280, corner_radius=0, fg_color="#1A1A1A", *args, **kwargs)

        # params
        self.printer = printer

        # header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=18, pady=(15, 10))

        ctk.CTkLabel(header, text="esc/pos app", font=("Arial", 24, "bold")).pack(anchor="w", pady=0)

        # connection
        connection_card = ctk.CTkFrame(self, fg_color="#222222", corner_radius=12)
        connection_card.pack(side="top", fill="x", padx=12, pady=(4, 0))

        # port select
        com_label = ctk.CTkLabel(connection_card, text="select port", font=("Arial", 12))
        com_label.pack(anchor="w", padx=14, pady=(7, 0))

        self.com_menu = ctk.CTkOptionMenu(connection_card, values=["COM?"],
            height=36, corner_radius=8, fg_color="#303030", button_color="#303030",
            button_hover_color="#3F3F3F", dropdown_fg_color="#252525",
            dropdown_hover_color="#3A3A3A", font=("Arial", 12))
        self.com_menu.pack(fill="x", padx=10, pady=(3, 12))
        self.com_menu.bind("<Enter>", self.refresh_com_menu)

        # printer connect
        connect_button = ctk.CTkButton(connection_card, text="connect to printer", height=38, corner_radius=8, font=("Arial", 12, "bold"), command=self.connect_printer)
        connect_button.pack(fill="x", padx=10, pady=(0, 14))

        self.refresh_com_menu()

    def refresh_com_menu(self, _=None):
        values = fetch_ports()

        if values:
            self.com_menu.configure(values=values)

    def get_selected_port(self):
        selected_text = self.com_menu.get()
        if "|" in selected_text:
            return selected_text.split("|")[0].strip()
        return selected_text.strip()
    
    def connect_printer(self):
        try:
            profile = Profile("./profiles/nixdorf_nd77.json") # TODO: profile selection
            port = self.get_selected_port()
        
            self.printer.connect(port, profile)

        except Exception as e:
            tk.messagebox.showerror(
                "connection error",
                f"failed to connect to printer.\n\n{type(e).__name__}: {e}",
                parent=self)