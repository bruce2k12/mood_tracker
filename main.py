import json
from datetime import datetime
import os

LOG_MOOD = 1
VIEW_MOOD_HISTORY = 2
ANALYZE_MOODS = 3
EXPORT_MOODS_TO_TXT = 4
EXIT = 5


def log_mood():  # Input and save a mood with a timestamp.
    mood_options = ["Anxious", "Calm", "Bitter", "Gloomy", "Cheerful", "Dubitative", "Lonely", "Stressed", "Anger",
                    "Fear", "Content", "Love", "Depressed mood", "Empathetic", "Mad", "Sadness", "Happiness",
                    "Enjoyment", "Disgust", "Imperative", "Mysterious"]
    print("How are you feeling Today ?")
    for i, mood in enumerate(mood_options, start=1):
        print(f"{i}. {mood}")

    try:
        choice = int(input("Hello please select a mood that you are feeling today: "))
        if 1 <= choice <= len(mood_options):
            selected_mood = mood_options[choice - 1]
            timestamp = datetime.now().strftime("%Y-%m-%d %I:%M %p")
            return {"timestamp": timestamp, "mood": selected_mood}
        else:
            print("Invalid Choice!")
            return None
    except ValueError:
        print("Please Enter a Number.")
        return None


def save_moods(moods):  # Write data to a JSON file
    with open("moods.json", "w") as file:
        json.dump(moods, file, indent=2)


def load_moods():  # Read and return data from the JSON file
    try:
        if os.path.exists("moods.json"):
            with open("moods.json", "r") as file:
                return json.load(file)
        else:
            return []
    except Exception as e:
        print("Error loading moods:", e)
        return []


def view_moods_history():  # Display past moods cleanly
    moods = load_moods()
    if not moods:
        print("No mood History yet.")
        return
    else:
        for mood_entry in moods:
            print(f"[{mood_entry['timestamp']}] - {mood_entry['mood']}")


def export_moods_to_text():
    moods = load_moods()
    if not moods:
        print("No moods to export!")
        return

    with open("mood_log.txt", "w") as file:
        file.write("Mood Log\n")
        file.write("=" * 20 + "\n")
        for mood in moods:
            file.write(f"[{mood['timestamp']}] - {mood['mood']}\n")

    print("Mood log exported to mood_log.txt")


def analyze_moods():
    moods = load_moods()
    if not moods:
        print("No mood data to analyze")
        return

    mood_counts = {}

    for entry in moods:
        mood = entry["mood"]
        if mood in mood_counts:
            mood_counts[mood] += 1
        else:
            mood_counts[mood] = 1

    print("\nMood Frequency:")
    for mood, count in mood_counts.items():
        print(f"{mood}: {count}")


def main():  # menu logic to drive app.
    mood_entries = load_moods()

    while True:
        print("\n1. Log a Mood\n2. View Mood History\n3. Analyze Moods\n4. Export Mood log to text file\n5. Exit")
        try:
            choice = int(input("Select a menu number to begin: "))
        except ValueError:
            print("Invalid Input. Please enter a number.")
            continue

        if choice == LOG_MOOD:
            mood = log_mood()
            if mood:
                mood_entries.append(mood)
                save_moods(mood_entries)
        elif choice == VIEW_MOOD_HISTORY:
            view_moods_history()
        elif choice == ANALYZE_MOODS:
            analyze_moods()
        elif choice == EXPORT_MOODS_TO_TXT:
            export_moods_to_text()
        elif choice == EXIT:
            print("Thank you for using the Mood Tracker!")
            break
        else:
            print("Invalid choice! Please select 1 - 5")


main()
