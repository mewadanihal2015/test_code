import os
import json
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

SAVE_FILE = "games.json"


class GameLauncher(ttk.Window):
    def __init__(self):
        super().__init__(themename="darkly")
        self.title("🎮 Game Launcher")
        self.geometry("700x500")
        self.resizable(False, False)

        self.games = []
        self.load_games()

        # --- Title Bar ---
        title = ttk.Label(self, text="🎮 Game Launcher", font=("Segoe UI", 24, "bold"))
        title.pack(pady=20)

        # --- Game List Frame ---
        self.frame = ttk.Frame(self)
        self.frame.pack(pady=10, fill=BOTH, expand=True)

        self.listbox = tk.Listbox(
            self.frame,
            font=("Segoe UI", 12),
            height=15,
            selectmode=tk.SINGLE,
            bg="#222",
            fg="white",
            selectbackground="#007bff",
            relief="flat"
        )
        self.listbox.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)

        scrollbar = ttk.Scrollbar(self.frame, command=self.listbox.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.listbox.config(yscrollcommand=scrollbar.set)

        # --- Button Frame ---
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="➕ Add Game", bootstyle=SUCCESS, width=15, command=self.add_game).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="🗑 Remove Game", bootstyle=DANGER, width=15, command=self.remove_game).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="▶ Launch Game", bootstyle=INFO, width=15, command=self.launch_game).grid(row=0, column=2, padx=5)
        ttk.Button(button_frame, text="💾 Save List", bootstyle=SECONDARY, width=15, command=self.save_games).grid(row=0, column=3, padx=5)

        # --- Footer ---
        ttk.Label(self, text="Made with ❤️ in Python", font=("Segoe UI", 9), bootstyle=SECONDARY).pack(side=BOTTOM, pady=5)

        self.refresh_list()

    # --- Methods ---
    def add_game(self):
        filepath = filedialog.askopenfilename(
            title="Select Game Executable",
            filetypes=(("Executable Files", "*.exe *.py"), ("All Files", "*.*"))
        )
        if filepath:
            name = os.path.basename(filepath)
            self.games.append({"name": name, "path": filepath})
            self.save_games()
            self.refresh_list()

    def remove_game(self):
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showinfo("Info", "Please select a game to remove.")
            return
        del self.games[selection[0]]
        self.save_games()
        self.refresh_list()

    def launch_game(self):
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showinfo("Info", "Select a game to launch.")
            return
        game = self.games[selection[0]]
        path = game["path"]
        try:
            if path.endswith(".py"):
                subprocess.Popen(["python", path])
            else:
                subprocess.Popen(path)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch game:\n{e}")

    def refresh_list(self):
        self.listbox.delete(0, tk.END)
        for g in self.games:
            self.listbox.insert(tk.END, g["name"])

    def save_games(self):
        with open(SAVE_FILE, "w") as f:
            json.dump(self.games, f, indent=4)

    def load_games(self):
        if os.path.exists(SAVE_FILE):
            with open(SAVE_FILE, "r") as f:
                self.games = json.load(f)


if __name__ == "__main__":
    app = GameLauncher()
    app.mainloop()
