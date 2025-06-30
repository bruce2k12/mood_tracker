import tkinter as tk
from tkinter import messagebox
from mood_data import mood_definitions
from datetime import datetime
import json
import os

root = tk.Tk()
root.title("Mood Tracker")
root.geometry("400x450")


def update_definition():
    mood = selected_mood.get()
    definition_label.config(text=f"{mood}: {mood_definitions[mood]}")


def log_mood_gui():
    mood = selected_mood.get()
    note = note_entry.get("1.0", tk.END).strip()
    timestamp = datetime.now().strftime("%Y-%m-%d %I:%M %p")

    mood_entry = {
        "timestamp": timestamp,
        "mood": mood,
        "note": note
    }

    # Save to JSON
    moods = []
    if os.path.exists("moods.json"):
        with open("moods.json", "r") as file:
            moods = json.load(file)
    moods.append(mood_entry)
    with open("moods.json", "w") as file:
        json.dump(moods, file, indent=2)

    messagebox.showinfo("Success", f"Mood '{mood}' logged!")
    note_entry.delete("1.0", tk.END)  # Clear text box


def show_mood_history():
    history_window = tk.Toplevel(root)
    history_window.title("Mood History")
    history_window.geometry("400x400")

    try:
        with open("moods.json", "r") as file:
            moods = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        moods = []

    if not moods:
        tk.Label(history_window, text="No mood history found.").pack(pady=20)
        return

    history_text = tk.Text(history_window, wrap=tk.WORD, width=50, height=20)
    history_text.pack(pady=10)

    for entry in moods:
        history_text.insert(tk.END, f"[{entry['timestamp']}] - {entry['mood']}\n")
        if entry.get("note"):
            history_text.insert(tk.END, f"Note: {entry['note']}\n")
        history_text.insert(tk.END, "\n")

    history_text.config(state=tk.DISABLED)


def export_moods_to_text():
    try:
        with open("moods.json", "r") as file:
            moods = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        messagebox.showerror("Error", "No mood data found.")
        return

    if not moods:
        messagebox.showinfo("Export", "No mood entries to export.")
        return

    with open("mood_log.txt", "w") as file:
        file.write("Mood Log\n")
        file.write("=" * 30 + "\n")
        for entry in moods:
            file.write(f"[{entry['timestamp']}] - {entry['mood']}\n")
            if entry.get("note"):
                file.write(f"Note: {entry['note']}\n")
            file.write("\n")

    messagebox.showinfo("Export", "Mood log exported to 'mood_log.txt'!")


# Heading
label = tk.Label(root, text="Welcome to Mood Tracker!", font=("Arial", 16))
label.pack(pady=20)

selected_mood = tk.StringVar()
selected_mood.set(next(iter(mood_definitions)))  # default first mood

mood_label = tk.Label(root, text="How are you feeling?")
mood_label.pack()

mood_dropdown = tk.OptionMenu(root, selected_mood, *mood_definitions.keys(), command=lambda _: update_definition())
mood_dropdown.pack(pady=5)

note_label = tk.Label(root, text="Optional: Add a journal note")
note_label.pack()

note_entry = tk.Text(root, height=4, width=40)
note_entry.pack(pady=5)

submit_button = tk.Button(root, text="Log Mood", command=lambda: log_mood_gui())
submit_button.pack(pady=10)

history_button = tk.Button(root, text="View Mood History", command=show_mood_history)
history_button.pack(pady=5)

export_button = tk.Button(root, text="Export to .txt", command=export_moods_to_text)
export_button.pack(pady=5)

definition_label = tk.Label(root, text="", wraplength=300, justify="left")
definition_label.pack()

# Keep window open
root.mainloop()
