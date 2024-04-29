import pytest
import unittest
from unittest.mock import patch, MagicMock, mock_open, call, ANY
import shutil
import tkinter as tk


# Import the functions to be tested
from BardicInspiration.feature_extraction import extract_music_data, process_folder, main, browse_folder, browse_output_csv, process_folder_gui

# Define test data
TEST_LABEL = "test_label"
TEST_OUTPUT_CSV = "test_output.csv"

@pytest.fixture
def test_folder(tmp_path):
    # Create a temporary directory
    folder_path = tmp_path / "test_folder"
    folder_path.mkdir()

    # Create test MIDI files
    test_files = ['song1.mid', 'song2.mid']
    for file in test_files:
        with open(folder_path / file, 'w') as f:
            f.write("Test MIDI data")

    return folder_path

class MockMidiTrack:
    def __init__(self, messages):
        self.messages = messages

    def __iter__(self):
        return iter(self.messages)

class MockMidiMessage:
    def __init__(self, message_type, time=0, **kwargs):
        self.type = message_type
        self.time = time  # Ensure 'time' attribute is set
        self.__dict__.update(kwargs)

def test_extract_music_data():
    # Define mocked MIDI data
    tempo_message = MockMidiMessage('set_tempo', time=0, tempo=50)
    time_signature_message = MockMidiMessage('time_signature', time=0, numerator=4, denominator=4)
    program_change_message = MockMidiMessage('program_change', time=0, program=1)  # Example program number
    key_signature_message = MockMidiMessage('key_signature', time=0, key='C')
    messages = [tempo_message, time_signature_message, program_change_message, key_signature_message]

    with patch('mido.MidiFile') as mock_midi_file:
        mock_midi_file_instance = mock_midi_file.return_value
        mock_midi_file_instance.tracks = [MockMidiTrack(messages)]

        features = extract_music_data("test.mid", TEST_LABEL)

        assert 'song_name' in features
        assert 'tempo' in features
        assert 'time_signature' in features
        assert 'instruments' in features
        assert len(features['instruments']) == 1  # Expecting one instrument
        assert 'key_signature' in features
        assert 'label' in features
        assert features['label'] == TEST_LABEL

def test_process_folder(test_folder):
    with patch('builtins.open', create=True) as mock_open:
        mock_open.side_effect = [MagicMock(), MagicMock()]

        process_folder(test_folder, TEST_LABEL, TEST_OUTPUT_CSV)

        assert mock_open.call_count == 2

def test_extract_music_data_nonexistent_file():
    # Pass a non-existent MIDI file path
    midi_file = "nonexistent.mid"
    label = "test_label"

    with pytest.raises(FileNotFoundError):
        extract_music_data(midi_file, label)

def test_process_folder_nonexistent_folder(tmp_path):
    # Pass a non-existent folder path
    folder_path = "/path/to/nonexistent/folder"
    label = "test_label"
    output_csv = "output.csv"

    with patch('builtins.open', create=True) as mock_open:
        # Mock the open function to prevent actual file creation
        mock_open.side_effect = FileNotFoundError

        with pytest.raises(FileNotFoundError):
            process_folder(folder_path, label, output_csv)

@pytest.fixture(scope="function")
def temp_dir(tmpdir):
    # Create a temporary directory
    yield tmpdir
    # Clean up the temporary directory after the test
    shutil.rmtree(str(tmpdir))

@pytest.fixture
def csv_file(tmp_path, monkeypatch):
    csv_path = tmp_path / "output.csv"

    # Define a function to mock the behavior of the open() function
    def mock_open_func(*args, **kwargs):
        if args[0] == str(csv_path):
            # If the open function is called with the csv_path, return a mock file object
            return mock_open()(*args, **kwargs)
        else:
            # Otherwise, call the original open function
            return open(*args, **kwargs)

    # Use monkeypatch to replace the behavior of the built-in open function
    with monkeypatch.context() as m:
        m.setattr("builtins.open", mock_open_func)
        # Return the path to the csv file
        return csv_path
    
def test_process_folder_error_message(temp_dir):
    with pytest.raises(FileNotFoundError):
        process_folder(str(temp_dir / "non_existent_folder"), "label", "output.csv")   

@pytest.fixture
def root():
    # Create a Tkinter root window
    root = tk.Tk()
    root.title("MIDI Music Data Extractor")
    yield root
    root.destroy()

class TestMainFunction(unittest.TestCase):
    @patch("BardicInspiration.feature_extraction.tk.Tk")
    @patch("BardicInspiration.feature_extraction.tk.Label")
    @patch("BardicInspiration.feature_extraction.tk.Entry")
    @patch("BardicInspiration.feature_extraction.tk.Button")
    def test_main(self, mock_button, mock_entry, mock_label, mock_tk):
        # Call the main function
        main()

        # Assert that the Tk constructor was called once
        mock_tk.assert_called_once()

        # Assert that the title method was called on the Tk instance
        mock_tk_instance = mock_tk.return_value
        mock_tk_instance.title.assert_called_once_with("MIDI Music Data Extractor")

        # Check that the necessary widgets were created and packed
        mock_label.assert_any_call(mock_tk_instance, text="Folder Path:")
        mock_label.assert_any_call(mock_tk_instance, text="Label:")
        mock_label.assert_any_call(mock_tk_instance, text="Output CSV:")
        mock_entry.assert_any_call(mock_tk_instance, width=40)
        mock_entry.assert_any_call(mock_tk_instance, width=40)
        mock_entry.assert_any_call(mock_tk_instance, width=40)

        # Check the commands for buttons
        browse_folder_button = [call(mock_tk_instance, text="Browse", name="browse_button", command=ANY)]
        browse_output_csv_button = [call(mock_tk_instance, text="Browse", name="browse_output_button", command=ANY)]
        process_folder_button = [call(mock_tk_instance, text="Process Folder", name="process_button", command=ANY)]

        self.assertIn(browse_folder_button, mock_button.mock_calls)
        self.assertIn(browse_output_csv_button, mock_button.mock_calls)
        self.assertIn(process_folder_button, mock_button.mock_calls)
        
    @patch("BardicInspiration.feature_extraction.filedialog.askdirectory", return_value="/path/to/folder")
    def test_browse_folder(self, mock_askdirectory):
        # Create a mock entry widget
        mock_entry = MagicMock()

        # Call the browse_folder function
        browse_folder(mock_entry)

        # Assert that askdirectory was called
        mock_askdirectory.assert_called_once()

        # Assert that the entry widget's methods were called
        mock_entry.delete.assert_called_once_with(0, ANY)
        mock_entry.insert.assert_called_once_with(ANY, "/path/to/folder")

    @patch("BardicInspiration.feature_extraction.filedialog.asksaveasfilename", return_value="/path/to/output.csv")
    def test_browse_output_csv(self, mock_asksaveasfilename):
        # Create a mock entry widget
        mock_entry = MagicMock()

        # Call the browse_output_csv function
        browse_output_csv(mock_entry)

        # Assert that asksaveasfilename was called
        mock_asksaveasfilename.assert_called_once_with(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])

        # Assert that the entry widget's methods were called
        mock_entry.delete.assert_called_once_with(0, ANY)
        mock_entry.insert.assert_called_once_with(ANY, "/path/to/output.csv")

    @patch("BardicInspiration.feature_extraction.process_folder")
    def test_process_folder_gui(self, mock_process_folder):
        # Create mock entry widgets
        mock_folder_path_entry = MagicMock()
        mock_label_entry = MagicMock()
        mock_output_csv_entry = MagicMock()

        # Set return values for get methods of entry widgets
        mock_folder_path_entry.get.return_value = "/path/to/folder"
        mock_label_entry.get.return_value = "label"
        mock_output_csv_entry.get.return_value = "/path/to/output.csv"

        # Call the process_folder_gui function
        process_folder_gui(mock_folder_path_entry, mock_label_entry, mock_output_csv_entry)

        # Assert that the process_folder function was called with correct arguments
        mock_process_folder.assert_called_once_with("/path/to/folder", "label", "/path/to/output.csv")
