import pickle
import numpy
import os
from music21 import note, stream, chord
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM, BatchNormalization, Activation
import tkinter as tk
from tkinter import ttk, messagebox

def generate_learned_midi_file():
    """This method will take the learning network at the code for notes and process them to create a new .midi file """
    if not os.path.exists("best_weights_loss.h5"):
        messagebox.showerror("Error", "No training weights file found.")
        return None, None, None, None, None
    with open("data/notes.pkl", "rb") as file:
        notes = pickle.load(file)
    
    pitch_names = sorted(set(item for item in notes))
    note_vocab = len(set(notes))

    net_input, norm_input = prepare_note_sequence(notes, pitch_names, note_vocab)
    lstm_model = create_neural_network(norm_input, note_vocab)
    music_output = create_music(lstm_model, net_input, pitch_names, note_vocab)

    return music_output, pitch_names, lstm_model, net_input, note_vocab

def prepare_note_sequence(notes, pitch_names, note_vocab):
    """Prepares the notes that will be used in the new music that is created"""
    note_to_integer = dict((note, number) for number, note in enumerate(pitch_names)) 

    number_of_notes = 100

    net_input = []
    music_output = []

    for i in range(0, len(notes) - number_of_notes, 1):
        sequence_in = notes[i:i + number_of_notes]
        sequence_out = notes[i + number_of_notes]
        net_input.append([note_to_integer[char] for char in sequence_in])  
        music_output.append(note_to_integer[sequence_out])

    note_patterns = len(net_input)

    norm_input = numpy.reshape(net_input, (note_patterns, number_of_notes, 1))
    norm_input = norm_input / float(note_vocab)

    return net_input, norm_input

def create_neural_network(net_input, note_vocab):
    """Creates the network and creates new music based on the training weights"""
    lstm_model = Sequential()
    lstm_model.add(LSTM(
        512,
        input_shape=(net_input.shape[1], net_input.shape[2]),  # Ensure correct input shape
        recurrent_dropout=0.3,
        return_sequences=True
    ))
    lstm_model.add(LSTM(512, return_sequences=True, recurrent_dropout=0.5))
    lstm_model.add(LSTM(512))
    lstm_model.add(BatchNormalization())
    lstm_model.add(Dropout(0.3))
    lstm_model.add(Dense(256))
    lstm_model.add(Activation('relu'))
    lstm_model.add(BatchNormalization())
    lstm_model.add(Dropout(0.3))
    lstm_model.add(Dense(note_vocab))
    lstm_model.add(Activation('softmax'))
    lstm_model.compile(loss='categorical_crossentropy', optimizer='rmsprop')

    lstm_model.load_weights("best_weights_loss.h5")

    return lstm_model

def create_music(lstm_model, net_input, pitch_names, note_vocab):
    """Creates music by using the LSTM model, note input, pitch input, and any other music information"""
    music_start = numpy.random.randint(0, len(net_input) - 1)

    integer_to_note = dict((number, note) for number, note in enumerate(pitch_names))

    pattern = net_input[music_start]
    pred_output = []

    for note_index in range(500):
        prediction_input = numpy.reshape(pattern, (1, len(pattern), 1))
        prediction_input = prediction_input / float(note_vocab)

        prediction = lstm_model.predict(prediction_input, verbose=0)

        # To add some randomness, you can use np.random.choice
        # to select the next note based on the predicted probabilities
        # This will give you more diverse output
        index = numpy.random.choice(len(prediction[0]), p=prediction[0])
        result = integer_to_note[index]
        pred_output.append(result)

        pattern.append(index)
        pattern = pattern[1:len(pattern)]
        
    # Convert Note objects to string representations
    pred_output = [str(note) for note in pred_output]

    return pred_output

def create_midi(pred_output):
    """Adds in notes, chords, or rests into the music"""
    output_notes = []
    offset = 0

    for pattern in pred_output:
        if pattern == 'R':
            new_note = note.Rest()
            new_note.offset = offset
            output_notes.append(new_note)
            offset += 0.5  # Adjust the offset for rests
        elif '.' in pattern:  # If it's a chord
            notes_in_chord = pattern.split('.')
            notes = []
            for current_note in notes_in_chord:
                new_note = note.Note(current_note)
                new_note.offset = offset
                notes.append(new_note)
            chord_note = chord.Chord(notes)
            chord_note.offset = offset
            output_notes.append(chord_note)
            # Increment the offset by the duration of the chord
            offset += chord_note.duration.quarterLength
        elif pattern.isdigit():  # If it's a single note
            new_note = note.Note(pattern)
            new_note.offset = offset
            output_notes.append(new_note)
            offset += 0.5  # Adjust the offset for single notes

    midi_stream = stream.Stream(output_notes)

    output_folder = "output"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    output_file_path = os.path.join(output_folder, "output.mid")
    midi_stream.write('midi', fp=output_file_path)

    messagebox.showinfo(f"Success!", "MIDI file generated: {output_file_path}")

def post_process_music(midi_stream, output_file_path):
    """Write the MIDI stream to a file"""
    midi_stream.write('midi', fp=output_file_path)

    messagebox.showinfo("Success", "Moving selected songs completed successfully.")

if __name__ == '__main__':
    music_output, pitch_names, lstm_model, net_input, note_vocab = generate_learned_midi_file()
    create_midi(music_output)