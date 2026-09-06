import customtkinter as ctk
import tkinter as tk

from .manager import AppManager

class Page(ctk.CTkFrame):
    def __init__(self, master, name: str, manager: AppManager, *args, **kwargs):
        super().__init__(master, fg_color="#181818", *args, **kwargs)

        self.manager = manager
        self.name = name

        self.printer = self.manager.printer
    
class TwoLayerDropdown(ctk.CTkFrame):
    item_height = 40

    item_subtitle_font = ("Arial", 9, "bold")
    item_title_font = ("Arial", 11)

    item_subtitle_color = "#8A8A8A"
    item_title_color = "#E5E5E5"

    item_fg_color = "transparent"
    item_selected_color = "#303030"
    item_hover_color = "#383838"

    def __init__(self, master, items: list[dict], command: callable | None = None, placeholder: str = "select item", **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        self.placeholder = placeholder

        self.items = items
        self.command = command

        self.selected_item = None
        self._popup = None

        self.button = ctk.CTkFrame(self, height=self.item_height, corner_radius=8, fg_color="#303030")
        self.button.pack(fill="x")
        self.button.pack_propagate(False)

        self._set_button_content()

    def _create_item_display(self, parent, item: dict):
        frame = ctk.CTkFrame(parent, height=self.item_height, fg_color="transparent")
        frame.pack_propagate(False)

        title = ctk.CTkLabel(frame, text=item.get("title", ""), font=self.item_title_font,
            text_color=self.item_title_color, anchor="w", height=10)
        title.pack(fill="x", padx=(8, 0), pady=(5, 0))

        subtitle = ctk.CTkLabel(frame, text=item.get("sub", ""), font=self.item_subtitle_font,
            text_color=self.item_subtitle_color, anchor="w", height=10)
        subtitle.pack(fill="x", padx=(8, 0), pady=(2, 0))

        return frame

    def _set_button_content(self):
        for widget in self.button.winfo_children():
            widget.destroy()

        item = self.selected_item or {"title": self.placeholder, "sub": ""}

        display = self._create_item_display(self.button, item)
        display.pack(fill="both", expand=True, padx=2, pady=1)

        self._bind_recursive(self.button, "<Button-1>", self._toggle_dropdown)

    def _bind_recursive(self, widget, sequence, callback):
        widget.bind(sequence, callback)

        for child in widget.winfo_children():
            self._bind_recursive(child, sequence, callback)

    def _toggle_dropdown(self, e = None):
        if self._popup is not None and self._popup.winfo_exists():
            self._close_dropdown()
        else:
            self._open_dropdown()

        return "break"

    def _open_dropdown(self):
        self.update_idletasks()

        self._popup = ctk.CTkToplevel(self)
        self._popup.overrideredirect(True)
        self._popup.configure(fg_color="#252525")

        x = self.button.winfo_rootx()
        y = self.button.winfo_rooty() + self.button.winfo_height() + 4
        width = self.button.winfo_width()

        content_height = len(self.items) * self.item_height + 10
        height = min(max(content_height, 90), 360)

        self._popup.geometry(f"{width}x{height}+{x}+{y}")

        frame = ctk.CTkFrame(self._popup, fg_color="#252525",
            corner_radius=8, border_width=1, border_color="#3A3A3A")
        frame.pack(fill="both", expand=True)

        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        item_frame = ctk.CTkScrollableFrame(frame, fg_color="transparent",
            corner_radius=0, scrollbar_button_color="#3A3A3A", scrollbar_button_hover_color="#484848")
        item_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        if not self.items:
            ctk.CTkLabel(item_frame, text="theres nothing :3", text_color="#777777", font=("Arial", 11)).pack(fill="x", pady=15)
        else:
            for item in self.items:
                self._create_item_button(item_frame, item)

        self._popup.lift()
        self._popup.update_idletasks()
        self._popup.grab_set()

    def _close_dropdown(self):
        popup = self._popup
        self._popup = None

        if popup is None:
            return

        try:
            popup.grab_release()
            popup.destroy()
        except tk.TclError:
            pass

    def _create_item_button(self, parent, item: dict):
        frame = ctk.CTkFrame(parent, height=self.item_height,
            corner_radius=7,
            fg_color=(
                self.item_selected_color
                if item is self.selected_item
                else self.item_fg_color
            )
        )
        frame.pack(fill="x", padx=2, pady=1)
        frame.pack_propagate(False)

        display = self._create_item_display(frame, item)
        display.pack(fill="both", expand=True)

        def select(e = None):
            self._select_item(item)
            return "break"

        def hover(e = None):
            frame.configure(fg_color=self.item_hover_color)

        def leave(e = None):
            frame.configure(
                fg_color=(
                    self.item_selected_color
                    if item is self.selected_item
                    else self.item_fg_color
                )
            )

        self._bind_recursive(frame, "<ButtonRelease-1>", select)

        frame.bind("<Enter>", hover)
        frame.bind("<Leave>", leave)

        for widget in display.winfo_children():
            widget.bind("<Enter>", hover)
            widget.bind("<Leave>", leave)

    def _select_item(self, item: dict):
        self.selected_item = item

        self._set_button_content()
        self._close_dropdown()

        if self.command:
            self.command(item)

class SwithcerRow(ctk.CTkFrame):
    def __init__(self, master, label, callback=None, *args, fg_color="transparent", **kwargs):
        super().__init__(master, fg_color=fg_color, *args, **kwargs)

        self.label = ctk.CTkLabel(self, text=label)
        self.label.grid(row=0, column=0, sticky="w")

        self.swithcer = ctk.CTkSwitch(self, text="", command=callback)
        self.swithcer.grid(row=0, column=1, padx=(10, 0))

        self.grid_columnconfigure(0, weight=1)