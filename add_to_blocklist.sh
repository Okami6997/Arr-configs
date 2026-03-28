#!/bin/bash

# Check if a file is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <path_to_text_file>"
    exit 1
fi

FILE=$1

# Check if file exists
if [ ! -f "$FILE" ]; then
    echo "Error: File '$FILE' not found."
    exit 1
fi

# Run the python script to add adlists
# We use python because sqlite3 command is not available and we need to modify gravity.db
sudo python3 /home/pi/add_adlists.py "$FILE"
