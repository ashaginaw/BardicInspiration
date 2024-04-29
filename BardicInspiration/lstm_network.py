"""We are creating and running our LSTM model to train our .midi files so we may produce music later. Since we are using
5 different folders, we will have to run this code for each catagory of music we have"""
"""This code was based off code from two people, Sigurður Skúli and Jordan Bird. However, their music generation
code is only for MIDI files with 1 instrument, and this is set to train on several instruments. Here are links
to their codes:  https://github.com/jordan-bird/Keras-LSTM-Music-Generator: Jordan Bird; 
https://github.com/Skuldur/Classical-Piano-Composer"""

import glob
import shutil
import numpy
import pickle
import tkinter as tk
from tkinter import filedialog
import csv
import os
from music21 import converter, note, chord
from keras.models import Sequential, clone_model
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.layers import Activation
from keras.layers import BatchNormalization
from tensorflow.python.keras.utils import np_utils
from keras.callbacks import ModelCheckpoint
from tkinter import messagebox

def train_neural_network(folder_path):
    """Method we will use to train the LSTM model with our music files"""
    output_folder = "data"  # Specify the set output folder for saving notes
    notes = get_notes(folder_path, output_folder)
    """Notes pulls in the list of notes we get from the get_notes method. get_notes is filled after we parse
    out each instrument for each piece of music that is being read in"""
    
    pitch_names = len(set(notes))

    music_input, music_output = music_creation(notes, pitch_names)

    lstm_model = create_network(music_input, pitch_names)

    train(lstm_model, music_input, music_output)

    print("Training neural network...")


def save_notes_to_file(notes, output_file_path):
    """Save notes to a file using pickling."""
    with open(output_file_path, 'wb') as output_file:
        pickle.dump(notes, output_file)

def get_notes(folder_path, output_folder):
    """Method to go through the MIDI files in the specified folder, parse notes from all instruments, and save them to a single file."""
    notes = []

    print("Folder path:", folder_path)

    # Check if folder exists
    if not os.path.exists(folder_path):
        print("Error: Folder does not exist")
        return notes

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for file in glob.glob(os.path.join(folder_path, "*.mid")):
        try:
            print("Parsing MIDI file:", file)
            midi_files = converter.parse(file)

            # Print information about the MIDI file
            print("Number of parts:", len(midi_files.parts))
            for part in midi_files.parts:
                print("Part:", part.partName)

                # Iterate over each note in the part
                for element in part.recurse().notes:
                    if isinstance(element, note.Rest):
                        notes.append('Rest')
                    elif isinstance(element, note.Note):
                        notes.append(str(element.pitch))
                    elif isinstance(element, chord.Chord):
                        chord_notes = '.'.join(note.Note(pitch).nameWithOctave for pitch in element.normalOrder)
                        notes.append('.'.join([chord_notes]))

        except Exception as e:
            print("Error parsing MIDI file:", file)
            print(e)

    if not notes:
        print("No notes found in MIDI files.")
    else:
        output_file_path = os.path.join(output_folder, "notes.pkl")
        save_notes_to_file(notes, output_file_path)
        print(f"All notes saved to: {output_file_path}")

    return notes

def music_creation(notes, pitch_names): 
    """We are preparing the music to be put into the LSTM Neural Network after the MIDI files have been parsed
    into notes and chords"""

    number_of_notes = 100
    if len(notes) <= number_of_notes:
        raise ValueError("Not enough notes to create music sequences")

    pitches = sorted(set(item for item in notes))   
    
    note_to_integer = dict((note, number) for number, note in enumerate(pitches))   
        
    music_input = []
    music_output = []

    for i in range(0, (len(notes) - number_of_notes), 1):
        sequence_in = notes[i:i + number_of_notes]
        sequence_out = notes[i + number_of_notes]
        music_input.append([note_to_integer[char] for char in sequence_in])  
        music_output.append([note_to_integer[sequence_out]])  # Wrap single note in a list

 
    note_patterns = len(music_input)
    
    music_input = numpy.reshape(music_input, (note_patterns, number_of_notes, 1))

    music_input = music_input / float(pitch_names)

    music_output = np_utils.to_categorical(music_output, num_classes=pitch_names)  # Convert to categorical with correct number of classes

    return music_input, music_output


def create_network(music_input, pitch_names):
    """We are putting in our parameters for how we want the structure of out Long Short-Term Memory Network
    to look"""

    lstm_model = Sequential()
    lstm_model.add(LSTM(
        512,
        input_shape = (music_input.shape[1], music_input.shape[2]),
        recurrent_dropout=0.2,
        return_sequences= True
        ))
    lstm_model.add(LSTM(512, return_sequences=True, recurrent_dropout=0.2))
    lstm_model.add(LSTM(512))
    lstm_model.add(BatchNormalization())
    lstm_model.add(Dropout(0.2))
    lstm_model.add(Dense(256))
    lstm_model.add(Activation('relu'))
    lstm_model.add(BatchNormalization())
    lstm_model.add(Dropout(0.2))
    lstm_model.add(Dense(pitch_names))
    lstm_model.add(Activation('softmax'))
    lstm_model.compile(loss = 'categorical_crossentropy', optimizer= 'rmsprop')

    return lstm_model

def train(lstm_model, music_input, music_output):
    """Method where we use our MIDI files to train the network so we can create original songs. This creates
    a .hdf5 file which we can use to populate music from the network"""

    best_loss_difference = float('inf')
    best_epoch_weights = None

    for epoch in range(100):  
        history = lstm_model.fit(music_input, music_output, epochs=1, batch_size=32, verbose=1)

        current_loss = history.history['loss'][0]
        loss_difference = abs(current_loss - 0.2)

        if loss_difference < best_loss_difference:
            best_loss_difference = loss_difference
            best_epoch_weights = lstm_model.get_weights()

    # Save the weights of the epoch with the loss closest to 0.2
    if best_epoch_weights is not None:
        lstm_model.set_weights(best_epoch_weights)
        lstm_model.save_weights("best_weights_loss.h5")

def train_model(output_folder):
    """Takes the selected songs and runs it through the LSTM model"""
    try:
        if output_folder:
            train_neural_network(output_folder)
            messagebox.showinfo("Success!", "Training completed successfully.")
        else:
            print("Please select an output folder first.")
    except Exception as e:
        print("Error during training:", e)

def move_selected_songs(csv_file_path, midi_folder, output_folder):
    try:
        if midi_folder and output_folder:
            # Only open 'selected_songs.csv' within the with statement
            with open(csv_file_path, 'r') as csv_file:
                csv_reader = csv.reader(csv_file)
                selected_songs = [row[0] for row in csv_reader]

            if not selected_songs:
                raise ValueError("No songs selected.")

            # Clear the output folder before moving new songs
            for file in os.listdir(output_folder):
                file_path = os.path.join(output_folder, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)

            moved_songs = []  # Track successfully moved songs
            for song in selected_songs:
                midi_file_path = os.path.join(midi_folder, song + '.mid')
                if os.path.exists(midi_file_path):
                    # Move the MIDI file to the output folder
                    destination_path = os.path.join(output_folder, song + '.mid')
                    shutil.copyfile(midi_file_path, destination_path)
                    moved_songs.append(song)
                    print(f"Moved {song}.mid to {output_folder}")
                else:
                    print(f"MIDI file '{song}.mid' not found in the selected folder.")
            if moved_songs:
                # Display success message only if songs were moved
                messagebox.showinfo("Success", "Moving selected songs completed successfully.")
            else:
                # No songs were moved, display error message
                messagebox.showinfo("Error", "No songs were moved.")
        else:
            raise ValueError("MIDI folder and output folder are not set.")
    except Exception as e:
        print("Error during moving selected songs:", e)
        messagebox.showinfo("Error", "An error occurred while moving selected songs.")

class MusicGeneratorApp:
    """This class holds the code for the page where the LSTM model will run."""
    def __init__(self, root):
        """Starts the code to generate the window, but allows us to add buttons and other features"""
        self.root = root
        """Code that starts the application window"""
        self.root.title("Music Generator")
        self.root.geometry("600x400")  # Larger window size

        self.midi_folder = "MIDI Music"
        """This folder holds the music within the application"""

        self.canvas= tk.Canvas(root, width=600, height=400, bg="slategray")
        """This allows us to add certain features to the window, such as a background color"""
        self.canvas.create_text(300, 100, font=("Fixedsys", 11), fill="Grey1", text= "Click Move Selected Songs to load them into our Machine Learning Program.\nAfter, Select train model. \nFinally, click Gimme My Music! for your final product!", justify='center')
        self.canvas.pack()

        # Set default values for CSV file and output folder
        self.csv_file_path = 'selected_songs.csv'
        self.output_folder = 'Selected MIDI Files'

        # Create a button to move selected songs
        self.move_songs_button = tk.Button(root, text="Move Selected Songs", command=lambda: move_selected_songs(self.csv_file_path, self.midi_folder, self.output_folder))
        """Runs the code to move the MIDI songs into the LSTM model"""
        self.move_songs_button.place(relx=0.3, rely=0.6, anchor='center')

        # Create a button to start training
        self.train_button = tk.Button(root, text="Train Model", command=lambda: train_model(self.output_folder))
        """This will add a buttont that will run the LSTM model on the selected music"""
        self.train_button.place(relx=0.5, rely=0.6, anchor='center')

        def music_creation_callback():
            os.system('python music_creation.py')

        self.create_button = tk.Button(root, text="Gimme My Music!", command=music_creation_callback)
        """This button starts the code for creating the new music based on training"""
        self.create_button.place(relx=0.7, rely=0.6, anchor='center')

    def browse_csv(self):
        """This starts a csv file with the names of the selected songs"""
        csv_file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        print("Selected CSV file:", csv_file_path)
        self.csv_file_path = csv_file_path
        self.csv_status.config(text="Success!")
        # Read and store the selected song names from the CSV file
        self.selected_songs = self.read_csv(csv_file_path)

    def browse_folder(self):
        """User selects the folder with the MIDI Music in it."""
        folder_path = filedialog.askdirectory()
        print("Selected MIDI Folder:", folder_path)
        self.selected_folder = folder_path
        self.folder_status.config(text="Success!")

    def browse_output_folder(self):
        """Allows user to select where they want the selected songs to be saved"""
        output_folder = filedialog.askdirectory()
        print("Selected Output Folder:", output_folder)
        self.output_folder = output_folder
        self.output_status.config(text="Success!")
    
    def move_midi_files(self):
        """Moves the MIDI files needed for training"""
        if self.csv_file_path:
            self.move_selected_songs()
        else:
        # Fall back to the original behavior of moving all MIDI files
            super().move_midi_files()

    def read_csv(self, csv_file_path):
        """Read the lists of songs in the csv and adds the selected songs to a folder"""
        songs = []
        with open(csv_file_path, 'r') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                songs.extend(row)
        return songs
    
if __name__ == "__main__":
    root = tk.Tk()
    app = MusicGeneratorApp(root)
    root.mainloop()
