import tkinter as tk
from tkinter import filedialog, messagebox, Listbox
import json
import os
import subprocess

# File to save game list
SAVE_FILE = "games.json"

class GameLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("Game Launcher")
        self.root.geometry("500x400")
        
        self.games = []
        self.load_games()

        # UI Setup
        tk.Label(root, text="🎮 Game Launcher", font=("Arial", 18, "bold")).pack(pady=10)

        self.listbox = Listbox(root, width=50, height=12)
        self.listbox.pack(pady=10)

        btn_frame = tk.Frame(root)
        btn_frame.pack()

        tk.Button(btn_frame, text="Add Game", command=self.add_game, width=12).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Remove Game", command=self.remove_game, width=12).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Launch Game", command=self.launch_game, width=12).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Exit", command=root.quit, width=12).grid(row=0, column=3, padx=5)

        self.refresh_list()

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
        selected = self.listbox.curselection()
        if selected:
            del self.games[selected[0]]
            self.save_games()
            self.refresh_list()
        else:
            messagebox.showinfo("Info", "Please select a game to remove.")

    def launch_game(self):
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showinfo("Info", "Select a game to launch.")
            return
        
        game = self.games[selected[0]]
        path = game["path"]
        try:
            if path.endswith(".py"):
                subprocess.Popen(["python", path])
            else:
                subprocess.Popen(path)
        except Exception as e:
            messagebox.showerror("Error", f"Could not launch game:\n{e}")

    def refresh_list(self):
        self.listbox.delete(0, tk.END)
        for game in self.games:
            self.listbox.insert(tk.END, game["name"])

    def save_games(self):
        with open(SAVE_FILE, "w") as f:
            json.dump(self.games, f, indent=4)

    def load_games(self):
        if os.path.exists(SAVE_FILE):
            with open(SAVE_FILE, "r") as f:
                self.games = json.load(f)

# Run launcher
if __name__ == "__main__":
    root = tk.Tk()
    app = GameLauncher(root)
    root.mainloop()
