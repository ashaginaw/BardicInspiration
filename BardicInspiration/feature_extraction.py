import tkinter as tk
from tkinter import filedialog
import os
import mido
import csv

def extract_music_data(midi_file, label):
    """This code will take out the important information we need, such as tempo, instruments, time signature, and key signature"""
    features = {}
    song_name = os.path.splitext(os.path.basename(midi_file))[0]
    features['song_name'] = song_name
    midi = mido.MidiFile(midi_file)
    tempo_changes = 0
    total_time = 0
    for track in midi.tracks:
        for message in track:
            if message.type == 'set_tempo':
                features['tempo'] = mido.tempo2bpm(message.tempo)
            elif message.type == 'time_signature':
                features['time_signature'] = f"{message.numerator}/{message.denominator}"
            elif message.type == 'program_change':
                if 'instruments' not in features:
                    features['instruments'] = []
                features['instruments'].append(message.program)
            elif message.type == 'key_signature':
                features['key_signature'] = message.key
            total_time += message.time
    features['label'] = label
    return features

def process_folder(folder_path, label, output_csv):
    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"Folder '{folder_path}' does not exist.")
    is_new_file = not os.path.exists(output_csv)
    try:
        with open(output_csv, 'a', newline='') as csvfile:
            fieldnames = ['song_name', 'tempo', 'time_signature', 'instruments', 'key_signature', 'label']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if is_new_file:
                writer.writeheader()
            for filename in os.listdir(folder_path):

                features = extract_music_data(os.path.join(folder_path, filename), label)
                writer.writerow(features)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Error processing folder: {e}")
    except EOFError:
        print("An error occurred while processing the file. Please check your file.")

def browse_folder(folder_path_entry):
    """Allows user to select the folder with the MIDI files."""
    folder_selected = filedialog.askdirectory()
    folder_path_entry.delete(0, tk.END)
    folder_path_entry.insert(tk.END, folder_selected)

def browse_output_csv(output_csv_entry):
    """Allows user to select the output CSV file."""

    file_selected = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    output_csv_entry.delete(0, tk.END)
    output_csv_entry.insert(tk.END, file_selected)

def process_folder_gui(folder_path_entry, label_entry, output_csv_entry):
    """Gets input from GUI and calls process_folder."""
    folder_path = folder_path_entry.get()
    label = label_entry.get()
    output_csv = output_csv_entry.get()
    process_folder(folder_path, label, output_csv)

def main():
    root = tk.Tk()
    root.title("MIDI Music Data Extractor")

    # Create and place labels and entries for folder path, label, and output CSV
    folder_label = tk.Label(root, text="Folder Path:")
    folder_label.pack(padx=5, pady=5, anchor="center")
    folder_path_entry = tk.Entry(root, width=40)
    folder_path_entry.pack(padx=5, pady=5)
    browse_folder_button = tk.Button(root, text="Browse", name="browse_button", command=lambda: browse_folder(folder_path_entry))
    browse_folder_button.pack(padx=5, pady=5)

    label_label = tk.Label(root, text="Label:")
    label_label.pack(padx=5, pady=5, anchor="center")
    label_entry = tk.Entry(root, width=40)
    label_entry.pack(padx=5, pady=5)

    output_csv_label = tk.Label(root, text="Output CSV:")
    output_csv_label.pack(padx=5, pady=5, anchor="center")
    output_csv_entry = tk.Entry(root, width=40)
    output_csv_entry.pack(padx=5, pady=5)
    browse_output_csv_button = tk.Button(root, text="Browse", name="browse_output_button", command=lambda: browse_output_csv(output_csv_entry))
    browse_output_csv_button.pack(padx=5, pady=5)

    process_button = tk.Button(root, text="Process Folder", name="process_button", command=lambda: process_folder_gui(folder_path_entry, label_entry, output_csv_entry))
    process_button.pack(padx=5, pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()