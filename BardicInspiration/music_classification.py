import csv
import tkinter as tk
from tkinter import messagebox

def process_csv(csv_file):
    """Process a CSV file containing music information and return a dictionary."""
    music_info = {}
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            piece_name = row['song_name'] 
            tempo = row['tempo']
            if tempo.lower() in ['unknown', '']:
                tempo = -1
            else:
                try:
                    tempo = float(tempo)
                except ValueError:
                    print("Invalid tempo value:", tempo)
                    tempo = -1
            row['tempo'] = tempo
            instruments = [instrument.strip() for instrument in row['instruments'].split(';')]
            music_info[piece_name] = {
                'Tempo': tempo,
                'Time Signature': row['time_signature'],
                'Instruments': instruments,  # Convert string representation of list to list
                'Key Signature': row['key_signature'],
                'Label': row['label']
            }
    return music_info

def music_search(selected_tempo, selected_time, selected_instrument, selected_key, selected_label, music_info):
    """Perform a search for music based on user-selected criteria."""

    tempo_ranges = {
        "0-60": (0.0, 60.0),
        "61-120": (61.0, 120.0),
        "121-180": (121.0, 180.0),
        "181+": (181.0, float('inf'))  # Using float('inf') to represent infinity
    }

    music_selected = []
    for song, attributes in music_info.items():
        if selected_instrument == "Any" or selected_instrument in attributes["Instruments"]:
            if (selected_time == "Any" or attributes["Time Signature"] == selected_time) and \
               (selected_key == "Any" or attributes["Key Signature"] == selected_key) and \
               (selected_label == "Any" or attributes["Label"].lower() == selected_label.lower()):  # Case-insensitive comparison
                if selected_tempo == "Any":
                    music_selected.append(song)
                else:
                    min_tempo, max_tempo = tempo_ranges[selected_tempo]
                    if min_tempo <= attributes["Tempo"] <= max_tempo:
                        music_selected.append(song)

    return music_selected

def perform_search_function(selected_tempo, selected_time, selected_instrument, selected_key, selected_label):
    """Once a user makes their selection, perform_search_functions will take the criteria and compare each song
    to it. If it matches, it goes into the newly created search_results.csv file"""

    music_info = process_csv('music_features.csv')

    selected_music = music_search(selected_tempo, selected_time, selected_instrument, selected_key, selected_label, music_info)

    if selected_music:
        # Write selected songs to a CSV file
        with open('selected_songs.csv', 'w', newline='') as csvfile:
            fieldnames = ['Song Name']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for song in selected_music:
                writer.writerow({'Song Name': song})

        messagebox.showinfo("Success", f"{len(selected_music)} songs found and saved to selected_songs.csv")
    else:
        messagebox.showinfo("No Results", "No songs found matching the criteria.")

def music_gui():
    root = tk.Tk()
    root.title("Bardic Inspiration")

    frame = tk.Frame(root)
    frame.pack(pady=20)

    # Canvas with background color and text
    canvas = tk.Canvas(frame, width=600, height=100, bg="slategray")
    canvas.create_text(300, 50, font=("Arial", 14, "bold"), fill="white",
                       text="Select the attributes for your music")
    canvas.grid(row=0, columnspan=2)

    # StringVar variables for options
    tempo_var = tk.StringVar(root)
    tempo_var.set("Any")
    time_var = tk.StringVar(root)
    time_var.set("Any")
    instrument_var = tk.StringVar(root)
    instrument_var.set("Any")
    key_var = tk.StringVar(root)
    key_var.set("Any")
    situation_var = tk.StringVar(root)
    situation_var.set("Any")

    # Labels and OptionMenu widgets
    tk.Label(frame, text="Select Tempo:", font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=5, sticky="e")
    tempo_options = ["Any", "0-60", "61-120", "121-180", "181+"]
    tk.OptionMenu(frame, tempo_var, *tempo_options).grid(row=1, column=1, padx=5, pady=5, sticky="w")

    tk.Label(frame, text="Select Time Signature:", font=("Arial", 12)).grid(row=2, column=0, padx=5, pady=5, sticky="e")
    time_options = ["Any", "4/4", "3/4", "2/2", "6/8"]
    tk.OptionMenu(frame, time_var, *time_options).grid(row=2, column=1, padx=5, pady=5, sticky="w")

    tk.Label(frame, text="Select Instrument:", font=("Arial", 12)).grid(row=3, column=0, padx=5, pady=5, sticky="e")
    instrument_options = ["Any", "Piano", "Guitar", "Flute", "Trumpet", "Violin"]
    tk.OptionMenu(frame, instrument_var, *instrument_options).grid(row=3, column=1, padx=5, pady=5, sticky="w")

    tk.Label(frame, text="Select Key Signature:", font=("Arial", 12)).grid(row=4, column=0, padx=5, pady=5, sticky="e")
    key_options = ["Any", "A", "Am", "Bb", "C", "Cm", "D", "Dm", "Eb", "F#", "G"]
    tk.OptionMenu(frame, key_var, *key_options).grid(row=4, column=1, padx=5, pady=5, sticky="w")

    tk.Label(frame, text="Select Situation:", font=("Arial", 12)).grid(row=5, column=0, padx=5, pady=5, sticky="e")
    situation_options = ["Any", "Boss", "Sad", "Tavern", "Exploration", "Victory"]
    tk.OptionMenu(frame, situation_var, *situation_options).grid(row=5, column=1, padx=5, pady=5, sticky="w")

    # Define a function to perform the search with current options
    def perform_search():
        selected_tempo = tempo_var.get()
        selected_time = time_var.get()
        selected_instrument = instrument_var.get()
        selected_key = key_var.get()
        selected_label = situation_var.get()
        perform_search_function(selected_tempo, selected_time, selected_instrument, selected_key, selected_label)

    # Search button
    search_button = tk.Button(frame, text="Search", font=("Arial", 12), command=perform_search)
    search_button.grid(row=6, columnspan=2, pady=10)

    root.mainloop()

if __name__ == "__main__":
    music_gui()