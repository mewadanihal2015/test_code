import tkinter as tk
from tkinter import ttk, messagebox

class GraphicsSettingsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Graphics Settings")
        self.root.geometry("400x300")

        self.default_settings = {
            "Resolution": "1920x1080",
            "Fullscreen": True,
            "V-Sync": True,
            "Texture Quality": "High"
        }

        self.create_widgets()

    def create_widgets(self):
        # Resolution
        tk.Label(self.root, text="Resolution:").grid(row=0, column=0, sticky='w', padx=10, pady=10)
        self.resolution_var = tk.StringVar(value=self.default_settings["Resolution"])
        resolution_options = ["1920x1080", "1600x900", "1280x720", "1024x768"]
        self.resolution_menu = ttk.Combobox(self.root, textvariable=self.resolution_var, values=resolution_options)
        self.resolution_menu.grid(row=0, column=1)

        # Fullscreen
        tk.Label(self.root, text="Fullscreen:").grid(row=1, column=0, sticky='w', padx=10)
        self.fullscreen_var = tk.BooleanVar(value=self.default_settings["Fullscreen"])
        self.fullscreen_check = ttk.Checkbutton(self.root, variable=self.fullscreen_var)
        self.fullscreen_check.grid(row=1, column=1, sticky='w')

        # V-Sync
        tk.Label(self.root, text="V-Sync:").grid(row=2, column=0, sticky='w', padx=10)
        self.vsync_var = tk.BooleanVar(value=self.default_settings["V-Sync"])
        self.vsync_check = ttk.Checkbutton(self.root, variable=self.vsync_var)
        self.vsync_check.grid(row=2, column=1, sticky='w')

        # Texture Quality
        tk.Label(self.root, text="Texture Quality:").grid(row=3, column=0, sticky='w', padx=10)
        self.texture_var = tk.StringVar(value=self.default_settings["Texture Quality"])
        texture_options = ["Low", "Medium", "High", "Ultra"]
        self.texture_menu = ttk.Combobox(self.root, textvariable=self.texture_var, values=texture_options)
        self.texture_menu.grid(row=3, column=1)

        # Buttons
        apply_btn = ttk.Button(self.root, text="Apply", command=self.apply_settings)
        apply_btn.grid(row=5, column=0, pady=20)

        reset_btn = ttk.Button(self.root, text="Reset", command=self.reset_settings)
        reset_btn.grid(row=5, column=1)

    def apply_settings(self):
        current_settings = {
            "Resolution": self.resolution_var.get(),
            "Fullscreen": self.fullscreen_var.get(),
            "V-Sync": self.vsync_var.get(),
            "Texture Quality": self.texture_var.get()
        }
        messagebox.showinfo("Settings Applied", f"New settings applied:\n{current_settings}")

    def reset_settings(self):
        self.resolution_var.set(self.default_settings["Resolution"])
        self.fullscreen_var.set(self.default_settings["Fullscreen"])
        self.vsync_var.set(self.default_settings["V-Sync"])
        self.texture_var.set(self.default_settings["Texture Quality"])
        messagebox.showinfo("Settings Reset", "Settings have been reset to default.")

if __name__ == "__main__":
    root = tk.Tk()
    app = GraphicsSettingsApp(root)
    root.mainloop()
