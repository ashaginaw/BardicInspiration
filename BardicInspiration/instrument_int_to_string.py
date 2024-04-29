import csv
import json  # Importing json module to safely parse string representations of lists

# Define a function to convert integers or ranges to strings
def int_range_to_string(num):
    """For our music_classification code, we need instruments to be lists as the name of the instrument, not the number.
    Since we are only using a selection of instruments, I grouped them by type of instrument according to the 
    MIDI coding for instruments."""
    int_range_to_string_map = {
        range(0, 7): "Piano",
        range(8, 15): "Bells",
        range(16, 23): "Organ",
        range(24, 31): "Guitar",
        range(32, 39): "Bass",
        range(40, 47): "Violin",
        range(48, 55): "Voice",
        range(56, 63): "Trumpet",
        range(64, 71): "Reeds",
        range(72, 79): "Flute",
        range(80, 127): "Other"
        # Add more ranges and their corresponding strings as needed
    }

    # Parse string representation of lists
    if isinstance(num, str):
        try:
            num = json.loads(num)
        except json.JSONDecodeError:
            return "Unknown"

    # Handle list of integers
    if isinstance(num, list):
        result = []
        for n in num:
            for int_range, string_value in int_range_to_string_map.items():
                if n in int_range:
                    result.append(string_value)
                    break
            else:
                result.append("Unknown")
        return result
    # Handle single integer
    else:
        for int_range, string_value in int_range_to_string_map.items():
            if int(num) in int_range:
                return string_value
        return "Unknown"

# Read the CSV file
input_file = 'music_features.csv'
output_file = 'output.csv'

data = []
with open(input_file, 'r', newline='') as csvfile:
    reader = csv.reader(csvfile)
    header = next(reader)  # Read the header row
    data.append(header)  # Append the header row to the data list
    for row in reader:
        data.append(row)

# Find the index of the column with header 'instruments'
column_index_to_process = header.index('instruments')

# Replace integers or ranges with strings in the specified column
for row in data[1:]:  # Start from index 1 to skip the header row
    row[column_index_to_process] = int_range_to_string(row[column_index_to_process])

# Write the updated data to a new CSV file
with open(output_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(data)