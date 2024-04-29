import pytest
import csv
import tkinter as tk
from BardicInspiration.music_classification import process_csv, music_search, perform_search_function, music_gui
import unittest
import tempfile
from unittest.mock import patch, MagicMock, mock_open

def create_temporary_csv(data):
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
        writer = csv.writer(temp_file)
        writer.writerows(data)
    return temp_file.name

@pytest.fixture
def mock_messagebox():
    with patch('BardicInspiration.music_classification.messagebox') as mock:
        yield mock

def test_process_csv():
    # Testing that the dictionary creation is working
    example_csv_data = [
        ['song_name', 'tempo', 'time_signature', 'instruments', 'key_signature', 'label'],
        ['Piece1', '120', '4/4', 'Piano;Guitar', 'C', 'Exploration'],
        ['Piece2', '140', '3/4', 'Flute;Violin', 'Am', 'Tavern'],
        ['Piece3', '90', '2/4', 'Trumpet', 'F#', 'Boss Battle']
    ]
    expected_result = {
        'Piece1': {'Tempo': 120.0, 'Time Signature': '4/4', 'Instruments': ['Piano', 'Guitar'],
                   'Key Signature': 'C', 'Label': 'Exploration'},
        'Piece2': {'Tempo': 140.0, 'Time Signature': '3/4', 'Instruments': ['Flute', 'Violin'],
                   'Key Signature': 'Am', 'Label': 'Tavern'},
        'Piece3': {'Tempo': 90.0, 'Time Signature': '2/4', 'Instruments': ['Trumpet'],
                   'Key Signature': 'F#', 'Label': 'Boss Battle'}
    }
    temp_csv_file = create_temporary_csv(example_csv_data)
    assert process_csv(temp_csv_file) == expected_result

def test_process_csv_invalid_format():
    # Test the function with a CSV file that has an invalid format
    example_csv_data = [
        ['Piece Name', 'Tempo', 'Time Signature', 'Instruments', 'Key Signature', 'Label'],
        ['Piece1', '120', '4/4', '[Piano, Guitar]', 'C'],  # Missing 'Label' column
        ['Piece2', '140', '3/4', '[Flute, Violin]', 'Am', 'Tavern'],
    ]
    temp_csv_file = create_temporary_csv(example_csv_data)
    with pytest.raises(Exception): 
        process_csv(temp_csv_file)

def create_temporary_csv(data):
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
        writer = csv.writer(temp_file)
        writer.writerows(data)
    return temp_file.name

def test_process_csv_with_invalid_tempo():
    # Test the function with a CSV file that has an invalid tempo value
    example_csv_data = [
        ['song_name', 'tempo', 'time_signature', 'instruments', 'key_signature', 'label'],
        ['Piece1', 'abc', '4/4', 'Piano;Guitar', 'C', 'Exploration'],
        ['Piece2', '140', '3/4', 'Flute;Violin', 'Am', 'Tavern'],
    ]
    temp_csv_file = create_temporary_csv(example_csv_data)
    music_info = process_csv(temp_csv_file)
    
    # Assert that the tempo value for Piece1 is set to -1
    assert music_info['Piece1']['Tempo'] == -1

    # Assert that the tempo value for Piece2 is correctly parsed as 140
    assert music_info['Piece2']['Tempo'] == 140.0

@pytest.fixture
def sample_music_info():
    # Sample music data for testing purposes
    return {
        "Song1": {"Tempo": 120, "Time Signature": "4/4", "Instruments": ["Piano", "Guitar"], "Key Signature": "C", "Label": "Tavern"},
        "Song2": {"Tempo": 140, "Time Signature": "3/4", "Instruments": ["Flute", "Violin"], "Key Signature": "G", "Label": "Exploration"},
        "Song3": {"Tempo": 90, "Time Signature": "6/8", "Instruments": ["Trumpet"], "Key Signature": "Dm", "Label": "Sad"}
    }

def test_music_search_with_criteria(sample_music_info):
    # Test music_search with specific criteria
    selected_tempo = "61-120"
    selected_time = "4/4"
    selected_instrument = "Piano"
    selected_key = "C"
    selected_label = "Tavern"
    selected_music = music_search(selected_tempo, selected_time, selected_instrument, selected_key, selected_label, sample_music_info)
    assert selected_music == ["Song1"]

def test_music_search_with_no_results(sample_music_info):
    # Test music_search with criteria that should yield no results
    selected_tempo = "181+"
    selected_time = "4/4"
    selected_instrument = "Flute"
    selected_key = "Cm"
    selected_label = "Tavern"
    selected_music = music_search(selected_tempo, selected_time, selected_instrument, selected_key, selected_label, sample_music_info)
    assert selected_music == []

def test_music_search_with_any_criteria(sample_music_info):
    # Test music_search with "Any" criteria aka no selections made
    selected_tempo = "Any"
    selected_time = "Any"
    selected_instrument = "Any"
    selected_key = "Any"
    selected_label = "Any"
    selected_music = music_search(selected_tempo, selected_time, selected_instrument, selected_key, selected_label, sample_music_info)
    assert selected_music == ["Song1", "Song2", "Song3"]

def test_music_search_with_unknown_tempo(sample_music_info):
    # Test music_search with tempo marked as "unknown"
    sample_music_info["Song4"] = {"Tempo": "unknown", "Time Signature": "4/4", "Instruments": ["Piano"], "Key Signature": "C", "Label": "Tavern"}
    selected_tempo = "Any"
    selected_time = "4/4"
    selected_instrument = "Piano"
    selected_key = "C"
    selected_label = "Tavern"
    selected_music = music_search(selected_tempo, selected_time, selected_instrument, selected_key, selected_label, sample_music_info)
    assert "Song4" in selected_music

def test_music_search_extreme_tempo(sample_music_info):
    #Testing that there is a failure if a tempo value is too large
    sample_music_info["Song4"] = {"Tempo": "50000000000", "Time Signature": "4/4", "Instruments": ["Piano"], "Key Signature": "C", "Label": "Tavern"}
    selected_tempo = "181+"
    selected_time = "4/4"
    selected_instrument = "Piano"
    selected_key = "C"
    selected_label = "Tavern"
    with pytest.raises(TypeError):
        music_search(selected_tempo, selected_time, selected_instrument, selected_key, selected_label, sample_music_info)
