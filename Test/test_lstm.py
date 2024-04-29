import pytest
import os
import tempfile
import tkinter as tk
import unittest
from unittest.mock import patch, MagicMock, mock_open, call
from BardicInspiration.lstm_network import train_neural_network, get_notes, music_creation, create_network, train_model, move_selected_songs


@patch('BardicInspiration.lstm_network.get_notes')
@patch('BardicInspiration.lstm_network.music_creation')
@patch('BardicInspiration.lstm_network.create_network')
@patch('BardicInspiration.lstm_network.train')
def test_train_neural_network(mock_train, mock_create_network, mock_music_creation, mock_get_notes):
    folder_path = '/some/folder/path'
    notes = ['note1', 'note2', 'note3']
    music_input = 'mocked music input'
    music_output = 'mocked music output'

    mock_get_notes.return_value = notes
    mock_music_creation.return_value = (music_input, music_output)

    train_neural_network(folder_path)

    mock_get_notes.assert_called_once_with(folder_path, 'data')
    mock_music_creation.assert_called_once_with(notes, len(set(notes)))
    mock_create_network.assert_called_once_with(music_input, len(set(notes)))
    mock_train.assert_called_once_with(mock_create_network.return_value, music_input, music_output)

def test_get_notes():
    with tempfile.TemporaryDirectory() as tmpdirname:
        midi_file_path = os.path.join(tmpdirname, "test.mid")
        with open(midi_file_path, 'w') as f:
            f.write("test MIDI file")

        notes = get_notes(tmpdirname, tmpdirname)

        assert len(notes) == 0

def test_music_creation():
    # Define input data
    notes = ['A', 'Ab', 'B', 'Bb', 'C#', 'C', 'D', 'Db', 'E', 'Eb', 'F', 'F#',
             'A', 'Ab', 'B', 'Bb', 'C#', 'C', 'D', 'Db', 'E', 'Eb', 'F', 'F#',
             'A', 'Ab', 'B', 'Bb', 'C#', 'C', 'D', 'Db', 'E', 'Eb', 'F', 'F#',
             'A', 'Ab', 'B', 'Bb', 'C#', 'C', 'D', 'Db', 'E', 'Eb', 'F', 'F#',
             'A', 'Ab', 'B', 'Bb', 'C#', 'C', 'D', 'Db', 'E', 'Eb', 'F', 'F#',
             'A', 'Ab', 'B', 'Bb', 'C#', 'C', 'D', 'Db', 'E', 'Eb', 'F', 'F#',
             'A', 'Ab', 'B', 'Bb', 'C#', 'C', 'D', 'Db', 'E', 'Eb', 'F', 'F#',
             'A', 'Ab', 'B', 'Bb', 'C#', 'C', 'D', 'Db', 'E', 'Eb', 'F', 'F#',
             'A', 'Ab', 'B', 'Bb', 'C#', 'C', 'D', 'Db', 'E', 'Eb', 'F', 'F#']
    pitch_names = 108

    # Call music_creation function
    music_input, music_output = music_creation(notes, pitch_names)

    # Assertions
    assert len(music_input) == len(notes) - 100  # Investigate if the correct number of input sequences is generated
    assert music_input.shape[2] == 1  # Investigate if the shape of input data is correct
    assert music_output.shape[1] == pitch_names  # Investigate if the shape of output data matches pitch names


def test_music_creation_not_enough_notes():
    # Define input data with fewer notes than required
    notes = ['C', 'D', 'E', 'F']  # Provide fewer notes than required for the sequence
    pitch_names = 4

    # Call music_creation function and expect it to raise a ValueError
    with pytest.raises(ValueError):
        music_input, music_output = music_creation(notes, pitch_names)

def test_create_network():
    # Define input data
    music_input = MagicMock()
    pitch_names = 10

    # Call create_network function
    lstm_model = create_network(music_input, pitch_names)

    # Assertions
    assert len(lstm_model.layers) == 11 

class TestMoveSelectedSongs(unittest.TestCase):
    def setUp(self):
        # Create temporary directories for test data
        self.temp_dir = tempfile.mkdtemp()
        self.midi_folder = os.path.join(self.temp_dir, 'test_folder')
        self.output_folder = os.path.join(self.temp_dir, 'test_midi')
        os.makedirs(self.midi_folder, exist_ok=True)
        os.makedirs(self.output_folder, exist_ok=True)

        # Create test MIDI files
        midi_files = ['song1.mid', 'song2.mid', 'song3.mid', 'song4.mid', 'song5.mid', 'song6.mid']
        for file in midi_files:
            with open(os.path.join(self.midi_folder, file), 'w') as f:
                f.write("Test MIDI content")

        # Create test CSV file
        self.csv_file_path = os.path.join(self.temp_dir, 'test.csv')
        with open(self.csv_file_path, 'w') as csv_file:
            csv_file.write("song1\nsong2\nsong3\nsong4\nsong5\nsong6")

    def test_move_selected_songs(self):
        
        # Call the function
        move_selected_songs(self.csv_file_path, self.midi_folder, self.output_folder)

        # Check if the MIDI files are moved to the output folder
        moved_files = os.listdir(self.output_folder)
        expected_files = ['song1.mid', 'song2.mid', 'song3.mid', 'song4.mid', 'song5.mid', 'song6.mid']
        self.assertCountEqual(moved_files, expected_files)

def test_train_model():
    output_folder = 'output_folder'

    with patch('BardicInspiration.lstm_network.train_neural_network') as mock_train_neural_network:
        # Call the function
        train_model(output_folder)

        # Assertions...
        mock_train_neural_network.assert_called_once_with(output_folder)