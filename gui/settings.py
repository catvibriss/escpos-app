import customtkinter as ctk
import tkinter as tk

from .objects import Page, SwithcerRow

from escpos import settings as esc_settings
from escpos.profile import Profile, CustomSetting
from escpos.utils import parse_command

class SettingsSection(ctk.CTkFrame):
    def __init__(self, master, title, width=600, *args, **kwargs):
        super().__init__(master, fg_color="#333333", corner_radius=10, width=width, *args, **kwargs)

        self._width = width
        
        title_font = ("Arial", 14)
        self.title = ctk.CTkLabel(self, text=title, font=title_font)  
        self.title.pack(anchor="w", padx=(8, 0), pady=(0, 0))

    def pack(self, *args, **kwargs):
        super().pack(*args, **kwargs)

        self.configure(width=self._width)
    
class CustomSettingGUI(ctk.CTkFrame):
    def __init__(self, master, setting: CustomSetting, *args, **kwargs):
        super().__init__(master, fg_color="transparent", *args, **kwargs)

        self.name = setting.name
        self.description = setting.description

        self.command = setting.command
        self.input_type = setting.input_type

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)

        self.label = ctk.CTkLabel(self, text=self.name)
        self.label.grid(row=0, column=0, sticky="w")

        self.input = None
        self._input_value = 0
        self._create_input()
        
    def _create_input(self):
        if self.input_type == "bool":
            self.input = ctk.CTkSwitch(self, text="")

        elif self.input_type.isdigit():
            maxinput = int(self.input_type)
            if maxinput < 0:
                return

            def _vcmd(v):
                return v == "" or (v.isdigit() and int(v) <= maxinput)

            self.input = ctk.CTkEntry(self, width=50, validate="key", validatecommand=(self.register(_vcmd), "%P"))
            
        self.input.grid(row=0, column=1, sticky="e")

    def get_command(self):
        return parse_command(self.command + f" {self._input_value}")

class Content(Page):
    def __init__(self, *args, **kwargs):
        super().__init__(name="settings", *args, **kwargs)

        ctk.CTkLabel(self, text="settings", font=("Arial", 24, "bold")).pack(anchor="w", pady=(15, 0))

        self.connect_printer_first = ctk.CTkLabel(self, text="connect your printer to unlock settings", font=("Arial", 14, "bold"), text_color="#ED6C6C")
        self.connect_printer_first.pack(anchor="w", pady=0)

        self.custom_settings = SettingsSection(self, "custom settings")
        self.custom_settings.pack(anchor="w", pady=(5, 0))

        self.manager.register_refreshable(self)
        self.refresh()

    def refresh(self):
        if self.manager.printer_connected:
            self._printer_connected()
        else:
            self._printer_disconnected()

    def _printer_connected(self):
        try: # TODO: set asb properly
            esc_settings.set_asb(self.printer, b"\xff")
        except: pass

        self.connect_printer_first.pack_forget()
        self._create_customs()

    def _printer_disconnected(self):
        self.connect_printer_first.pack()

    def _create_customs(self):
        customs = self.printer.profile.get_custom_settings()

        for custom in customs:
            csobj = CustomSettingGUI(self.custom_settings, custom)
            csobj.pack(fill="x", padx=8)