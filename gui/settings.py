from .objects import Page

class Content(Page):
    def __init__(self, *args, **kwargs):
        super().__init__(name="settings", *args, **kwargs)

            ctk.CTkLabel(self, text="settings", font=("Arial", 24, "bold")).pack(anchor="w", pady=(15, 0))

        self.connect_printer_first = ctk.CTkLabel(self, text="connect your printer to unlock settings", font=("Arial", 14, "bold"))
        self.connect_printer_first.pack(anchor="w", pady=0)

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

    def _printer_disconnected(self):
        self.connect_printer_first.pack()