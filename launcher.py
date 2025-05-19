import tkinter as tk
import os
import sys
import threading
import subprocess
from tkinter import messagebox, filedialog
from pystray import Icon, MenuItem, Menu
from PIL import Image, ImageTk

SETTINGS_FILE = "settings.txt"


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def main():
    root = tk.Tk()
    root.title("Eclipse Launcher")
    root.geometry("900x600")
    root.iconbitmap(resource_path("assets/logo.ico"))
    root.configure(bg="#1e1e1e")
    root.resizable(False, False)

    # Background image
    bg_image = Image.open(resource_path("assets/background.jpg")).resize((900, 600))
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(root, image=bg_photo)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    bg_label.image = bg_photo

    # Play button
    play_button = tk.Button(root, text="Play", font=("Arial", 20, "bold"), bg="#444444", fg="white", width=15, height=2, borderwidth=0, relief="flat", command=lambda: launch_game(root, play_button))
    play_button.place(relx=0.5, rely=0.5, anchor="center")
    play_button.bind("<Enter>", lambda e: play_button.configure(bg="#555555"))
    play_button.bind("<Leave>", lambda e: play_button.configure(bg="#444444"))

    # Settings button
    settings_image = Image.open(resource_path("assets/settings.png")).resize((40, 40))
    settings_icon = ImageTk.PhotoImage(settings_image)
    settings_button = tk.Button(root, image=settings_icon, borderwidth=0, relief="flat", bg="#1e1e1e", activebackground="#1e1e1e", command=lambda: open_settings_menu(root))
    settings_button.place(x=20, y=20)
    settings_button.image = settings_icon

    root.mainloop()


def launch_game(root, button):
    game_path = load_game_path()
    if game_path:
        try:
            subprocess.Popen([game_path])
            root.withdraw()  # Only hide if the game actually starts
            threading.Thread(target=hide_to_tray, args=(root,)).start()
        except FileNotFoundError:
            messagebox.showerror("The Abyss is Endless.", "Could not find the executable. Check your game path.")
    else:
        messagebox.showerror("The Abyss is Endless.", "Game path not set. Please set the game path in the settings.")


def hide_to_tray(root):
    icon_image = Image.open(resource_path("assets/logo.ico"))
    tray_icon = Icon("Eclipse Launcher", icon_image, menu=Menu(MenuItem("Exit", lambda: exit_launcher(root))))
    tray_icon.run()


def exit_launcher(root):
    root.quit()
    os._exit(0)


def load_game_path():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            return f.read().strip()
    return None


def save_game_path(path):
    with open(SETTINGS_FILE, "w") as f:
        f.write(path)


def open_settings_menu(root):
    settings_window = tk.Toplevel(root)
    settings_window.title("Settings")
    settings_window.geometry("300x400")
    settings_window.iconbitmap(resource_path("assets/logo.ico"))
    settings_window.configure(bg="#1e1e1e")

    tk.Label(settings_window, text="Settings", font=("Arial", 18, "bold"), bg="#1e1e1e", fg="white").pack(pady=20)
    tk.Button(settings_window, text="Change Game Path", font=("Arial", 14), bg="#444444", fg="white", command=lambda: change_game_path(root)).pack(pady=10)
    tk.Button(settings_window, text="View Game Path", font=("Arial", 14), bg="#444444", fg="white", command=view_game_path).pack(pady=10)
    tk.Button(settings_window, text="Reset Game Path", font=("Arial", 14), bg="#444444", fg="white", command=reset_game_path).pack(pady=10)
    tk.Button(settings_window, text="Close", font=("Arial", 14), bg="#555555", fg="white", command=settings_window.destroy).pack(pady=20)


def view_game_path():
    game_path = load_game_path()
    if game_path:
        messagebox.showinfo("Current Game Path", f"Current Game Path:\n{game_path}")
    else:
        messagebox.showwarning("No Game Path Set", "No game path is currently set. Please set the game path in the settings.")


def change_game_path(root):
    new_path = filedialog.askopenfilename(title="Select Game Executable", filetypes=[("Executables", "*.exe"), ("All Files", "*")])
    if new_path:
        save_game_path(new_path)
        messagebox.showinfo("Path Updated", "Game path updated successfully.")


def reset_game_path():
    if os.path.exists(SETTINGS_FILE):
        os.remove(SETTINGS_FILE)
        messagebox.showinfo("Reset Complete", "Game path reset successfully.")


if __name__ == "__main__":
    main()
