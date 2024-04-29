import unittest
from unittest.mock import Mock, patch, mock_open
import numpy as np
import tkinter as tk
from BardicInspiration.music_creation import *

class TestMusicGeneration(unittest.TestCase):
    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data="dummy_data")
    def test_prepare_note_sequence(self, mock_open):
        # Mock data and expected results
        notes = ["C", "D", "E", "F", "G",
                 "C", "D", "E", "F", "G",
                 "C", "D", "E", "F", "G",
                 "C", "D", "E", "F", "G",
                 "C", "D", "E", "F", "G",
                 "C", "D", "E", "F", "G",
                 "C", "D", "E", "F", "G",
                 "C", "D", "E", "F", "G",
                 "C", "D", "E", "F", "G",
                 "C", "D", "E", "F", "G",
                 "C", "D", "E", "F", "G",
                 "C", "D", "E", "F", "G",
                 "C", "D", "E", "F", "G",
                 "C", "D", "E", "F", "G",
                 "C", "D", "E", "F", "G",
                 "C", "D", "E", "F", "G",
                 "C", "D", "E", "F", "G",
                 "C", "D", "E", "F", "G",
                 "C", "D", "E", "F", "G",
                 "C", "D", "E", "F", "G"]
        pitch_names = ["C", "D", "E", "F", "G"]
        note_vocab = 5

        # Call the function to test
        net_input, norm_input = prepare_note_sequence(notes, pitch_names, note_vocab)

        # Assertions
        self.assertEqual(len(net_input), len(notes) - 100)
        self.assertEqual(norm_input.shape, (len(notes) - 100, 100, 1))

    @patch('keras.models.Sequential.load_weights')  # Mock the load_weights method
    @patch('os.path.exists', return_value=True)  # Mock os.path.exists to return True
    def test_create_neural_network(self, mock_exists, mock_load_weights):
        # Mock data
        net_input = np.random.rand(10, 100, 1)
        note_vocab = 100

        # Call the function to test
        lstm_model = create_neural_network(net_input, note_vocab)

        # Assertions
        assert len(lstm_model.layers) == 11
        mock_load_weights.assert_called_once_with("best_weights_loss.h5")

    @patch('music21.stream.Stream.write')
    @patch('tkinter.messagebox.showinfo')
    def test_create_midi(self, mock_showinfo, mock_write):
        # Mock data
        pred_output = ['C', 'D', 'E', 'F']
        instrument_name = "Violin"

        # Call the function to test
        create_midi(pred_output)

        # Assertions
        mock_showinfo.assert_called_once()
        mock_write.assert_called_once()

    """@patch('tkinter.StringVar.get', return_value="Violin")
    def test_start_process(self, mock_get):
        # Mocking some dependencies
        start_process()
        # Here you can add assertions to ensure correct behavior of the function."""

if __name__ == '__main__':
    unittest.main()