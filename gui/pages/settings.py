import customtkinter as ctk
import tkinter as tk

from gui.objects import Page, SwithcerRow

from escpos import settings as esc_settings
from escpos.profile import Profile, CustomSetting
from escpos.utils import parse_command

class CustomSettingGUI:
    def __init__(self, master, setting: CustomSetting, row):
        self.master = master

        self.name = setting.name
        self.description = setting.description

        self.command = setting.command
        self.input_type = setting.input_type

        self.label = ctk.CTkLabel(master, text=self.name)
        self.label.grid(row=row, column=0, sticky="w", padx=8, pady=4)

        self.input = None
        self._input_value = 0
        self._create_input(row)

    def _create_input(self, row):
        if self.input_type == "bool":
            self.input = ctk.CTkSwitch(self.master, text="", width=50)
            self.input.set(0)

        elif self.input_type.isdigit():
            maxinput = int(self.input_type)
            if maxinput < 0:
                return

            def _vcmd(v):
                return v == "" or (v.isdigit() and int(v) <= maxinput)

            self.input = ctk.CTkEntry(self.master, width=50, validate="key", validatecommand=(self.master.register(_vcmd), "%P"))
            self.input.insert(0, "0")

        self.input.grid(row=row, column=2, sticky="e", padx=8, pady=4)

    def get_command(self):
        return parse_command(self.command + f" {self._input_value}")

class CustomSettingsTable(ctk.CTkFrame):
    def __init__(self, master, printer, *args, **kwargs):
        super().__init__(master, fg_color="transparent", corner_radius=10, width=300, *args, **kwargs)

        self.printer = printer

        self.pack_propagate(False)

        self.settings = []

        self.content = ctk.CTkFrame(self, fg_color="transparent")
        self.content.pack(fill="both", expand=True)

        self.content.grid_columnconfigure(0, weight=0)
        self.content.grid_columnconfigure(1, weight=1)
        self.content.grid_columnconfigure(2, weight=0)

        self.title = ctk.CTkLabel(self.content, text="custom settings", font=("Arial", 14))
        self.title.grid(row=0, column=0, columnspan=3, sticky="w", padx=8, pady=(0, 4))

        self.no_settings = ctk.CTkLabel(self.content, text="no custom settings")
        self.no_settings.grid(row=1, column=0, columnspan=3, sticky="w", padx=8, pady=(4, 8))

        self._update_height()

    def load(self, customs):
        for setting in self.settings:
            setting.label.destroy()
            setting.input.destroy()

        self.settings.clear()

        self.no_settings.grid_forget()

        if hasattr(self, "apply_button"):
            self.apply_button.destroy()
            del self.apply_button

        if customs:
            for row, custom in enumerate(customs, start=1):
                setting = CustomSettingGUI(self.content, custom, row)
                self.settings.append(setting)

            self.apply_button = ctk.CTkButton(self.content, text="Apply", command=self._apply)
            self.apply_button.grid(row=len(self.settings) + 1, column=0, columnspan=3, sticky="w", padx=8, pady=(5, 8))
        else:
            self.no_settings.grid(row=1, column=0, columnspan=3, sticky="w", padx=8, pady=(4, 8))

        self._update_height()

    def _update_height(self):
        self.update_idletasks()
        self.configure(width=300, height=self.content.winfo_reqheight())

    def _apply(self):
        for setting in self.settings:
            setting._input_value = setting.input.get()
            self.printer.send(setting.get_command())

class Content(Page):
    def __init__(self, *args, **kwargs):
        super().__init__(name="settings", *args, **kwargs)

        ctk.CTkLabel(self, text="settings", font=("Arial", 24, "bold")).pack(anchor="w", pady=(15, 0))

        self.connect_printer_first = ctk.CTkLabel(self, text="connect your printer to unlock settings", font=("Arial", 14, "bold"), text_color="#ED6C6C")
        self.connect_printer_first.pack(anchor="w", pady=0)

        self.custom_settings = CustomSettingsTable(self, self.manager.printer)
        self.custom_settings.pack(anchor="w", pady=(10, 0))

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
        self.custom_settings.load(customs)