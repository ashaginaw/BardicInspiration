import os
import tempfile
import shutil
from unittest.mock import patch, MagicMock
import pytest
import unittest
import tkinter as tk

from BardicInspiration.file_upload import save_file, select_and_save_file, get_selected_file, show_message,setup_gui, on_close


@pytest.fixture(scope="module")
def temp_dir():
    # Create a temporary directory to use as the source folder
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    # Clean up the temporary directory after the tests
    shutil.rmtree(temp_dir)

@pytest.fixture(scope="module")
def temp_file(temp_dir):
    # Create a temporary MIDI file in the source folder
    temp_file_path = os.path.join(temp_dir, "test.mid")
    with open(temp_file_path, "w") as f:
        f.write("Test MIDI data")
    return temp_file_path

def test_save_file_success(temp_file, temp_dir):
    # Create a separate temporary directory to use as the destination folder

    dest_dir = tempfile.mkdtemp()
    try:
        # Call save_file with the temporary MIDI file selected and the separate destination folder
        success, message = save_file(temp_file, dest_dir)

        # Assert that the file was copied to the destination folder
        copied_file_path = os.path.join(dest_dir, "test.mid")
        assert os.path.exists(copied_file_path)

        # Assert that the function returns success and a correct message
        assert success is True
        assert "has been accepted and saved to 'MIDI Music' successfully." in message
    finally:
        # Clean up the separate temporary destination folder
        shutil.rmtree(dest_dir)

@patch("BardicInspiration.file_upload.get_selected_file", return_value="test.mid")  # Mock the get_selected_file function to return a file path
@patch("BardicInspiration.file_upload.save_file", return_value=(True, "File 'test.mid' has been accepted and saved to 'MIDI Music' successfully."))  # Mock the save_file function to return success
@patch("BardicInspiration.file_upload.show_message")  # Mock the show_message function
def test_select_and_save_file_success(mock_show_message, mock_save_file, mock_get_selected_file):
    # Call the select_and_save_file function
    select_and_save_file()

    # Assert that get_selected_file, save_file, and show_message were called with the correct arguments

    mock_get_selected_file.assert_called_once()
    mock_save_file.assert_called_once_with("test.mid", "MIDI Music")
    mock_show_message.assert_called_once_with("File Accepted", "File 'test.mid' has been accepted and saved to 'MIDI Music' successfully.")

@patch("BardicInspiration.file_upload.get_selected_file", return_value=None)  # Mock the get_selected_file function to return None (simulate canceling file selection)
@patch("BardicInspiration.file_upload.show_message")  # Mock the show_message function
def test_select_and_save_file_cancel(mock_show_message, mock_get_selected_file):
    # Call the select_and_save_file function
    select_and_save_file()

    # Assert that get_selected_file was called
    mock_get_selected_file.assert_called_once()
    # Assert that show_message was called with the correct arguments
    mock_show_message.assert_called_once_with("Error", "No file selected.")

# Mocking necessary dependencies
@patch("BardicInspiration.file_upload.shutil.copy", side_effect=shutil.copy)
def test_save_file_same_paths(mock_copy):
    # Define source and destination paths to be the same
    temp_file = 'C:\\Users\\amand\\AppData\\Local\\Temp\\temp.mid'
    temp_dir = 'C:\\Users\\amand\\AppData\\Local\\Temp\\'

    # Call save_file with the same source and destination paths
    success, message = save_file(temp_file, temp_dir)

    # Assert that the function returns False and the correct error message
    assert success is False
    assert message == "Source and destination paths are the same."

class TestSaveFile(unittest.TestCase):

    def test_save_file_no_file_selected(self):
        success, message = save_file(None, "destination_folder")
        self.assertFalse(success)
        self.assertEqual(message, "No file selected.")

    @patch('os.path.basename')
    @patch('os.path.join')
    @patch('shutil.copy')
    def test_save_file_exception(self, mock_copy, mock_join, mock_basename):
        mock_basename.side_effect = Exception("Test Exception")
        success, message = save_file("source_file", "destination_folder")
        self.assertFalse(success)
        self.assertEqual(message, "Test Exception")

class TestGetSelectedFile(unittest.TestCase):

    @patch('tkinter.filedialog.askopenfilename')
    def test_get_selected_file_file_selected(self, mock_askopenfilename):
        mock_askopenfilename.return_value = "selected_file.mid"
        file_path = get_selected_file()
        self.assertEqual(file_path, "selected_file.mid")

    @patch('tkinter.filedialog.askopenfilename')
    def test_get_selected_file_no_file_selected(self, mock_askopenfilename):
        mock_askopenfilename.return_value = None
        file_path = get_selected_file()
        self.assertEqual(file_path, None)

class TestShowMessage(unittest.TestCase):
    @patch('BardicInspiration.file_upload.messagebox.showinfo')
    def test_show_message(self, mock_showinfo):
        title = "Test Title"
        message = "Test Message"
        
        # Call the function
        show_message(title, message)
        
        # Assert that messagebox.showinfo was called with the correct arguments
        mock_showinfo.assert_called_once_with(title, message)

class TestSaveFile(unittest.TestCase):
    @patch('BardicInspiration.file_upload.os.path.basename')
    @patch('BardicInspiration.file_upload.os.path.join')
    @patch('BardicInspiration.file_upload.os.path.abspath')
    @patch('BardicInspiration.file_upload.shutil.copy')
    def test_save_file_no_file_selected(self, mock_copy, mock_abspath, mock_join, mock_basename):
        mock_basename.return_value = 'file.mid'
        mock_join.return_value = 'destination_folder/file.mid'
        mock_abspath.side_effect = lambda x: x
        
        # Call the function with source_file=None
        success, message = save_file(None, 'destination_folder')
        
        # Assert that the function returns False and the correct message
        self.assertFalse(success)
        self.assertEqual(message, "No file selected.")
        # Ensure shutil.copy is not called
        mock_copy.assert_not_called()

    @patch('BardicInspiration.file_upload.os.path.basename')
    @patch('BardicInspiration.file_upload.os.path.join')
    @patch('BardicInspiration.file_upload.os.path.abspath')
    @patch('BardicInspiration.file_upload.shutil.copy')
    def test_save_file_exception(self, mock_copy, mock_abspath, mock_join, mock_basename):
        mock_basename.return_value = 'file.mid'
        mock_join.return_value = 'destination_folder/file.mid'
        mock_abspath.side_effect = lambda x: x
        mock_copy.side_effect = Exception("Something went wrong")
        
        # Call the function with a valid source_file
        success, message = save_file('source_file.mid', 'destination_folder')
        
        # Assert that the function returns False and the correct error message
        self.assertFalse(success)
        self.assertEqual(message, "Something went wrong")

class TestSetupGUI(unittest.TestCase):
    @patch('BardicInspiration.file_upload.tk.Tk')
    @patch('BardicInspiration.file_upload.tk.Canvas')
    @patch('BardicInspiration.file_upload.tk.Button')
    def test_setup_gui(self, mock_button, mock_canvas, mock_tk):
        # Mock the on_close function
        mock_on_close = MagicMock()

        # Call the setup_gui function with the mock on_close function
        setup_gui(on_close=mock_on_close)

        # Check if Tkinter objects are created and configured correctly
        mock_canvas_instance = mock_canvas.return_value
        mock_canvas_instance.create_text.assert_called_once_with(250, 100, font=("Fixedsys", 11), fill="Grey1",
                           text="Click the button to select a MIDI file\nand save it to 'MIDI Music'",
                           justify="center")
        mock_canvas_instance.pack.assert_called_once_with()
        mock_button_instance = mock_button.return_value
        mock_button_instance.pack.assert_called_once_with()

        # Assert that the protocol method was called with the expected arguments
        mock_tk.return_value.protocol.assert_called_once_with("WM_DELETE_WINDOW", mock_on_close)
