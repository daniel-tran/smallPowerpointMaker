"""
Module for obtaining CCLI data"""
import csv
import os
import fuzzywuzzy
import fuzzywuzzy.fuzz
from helpers import scripts_folder, get_spreadsheet_to_csv_file

def find_ccli(song_title: str, ccli_file_name="ccli.csv", matching=12) -> str:
    '''
    Finds the required CCLI information for a song from a csv file. If no information found returns nothing

    CCLI information should be provided in the same directory as this file, 
    and the file should be organised as so:

    Song Name | Song CCLI message | Song CCLI number
    '''

    ccli_file_name = f'{scripts_folder}/{ccli_file_name}'
    song_title = song_title.replace("(live)", "").lower().strip()

    if not os.path.exists(ccli_file_name):
        get_spreadsheet_to_csv_file(os.environ.get("CCLI_URL"), ccli_file_name)

    with open(ccli_file_name, mode='r', newline='', encoding='utf-8') as csvfile:
        reader = list(csv.reader(csvfile))
        
        # Iterate over each row to find an exact match first
        for row in reader:
            song_name = row[0].lower().strip()

            # Prioritize an exact match
            if song_title == song_name:
                return f'{row[1]}. CCLI Song number: {row[2]}'
        
        # Iterate over each row for partial matches. 
        if len(song_title) < matching:
            # Iterate over each row for partial matches. 
            for row in reader:
                song_name = row[0].lower().strip()
                # Check if there is a partial match
                for i in range(len(song_name) - matching + 1):
                    if fuzzywuzzy.fuzz.partial_ratio(song_name[i:i+matching], song_title) > 80:
                        return f'{row[1]}. CCLI Song number: {row[2]}'

        for row in reader:
            song_name = row[0].lower().strip()
            # Check if there is a match
            for i in range(len(song_name) - matching + 1):
                if fuzzywuzzy.fuzz.partial_ratio(song_name[i:i+matching], song_title) > 80:
                    return f'{row[1]}. CCLI Song number: {row[2]}'

    # If no match is found, return just the ccli license number

    # Replace with your own CCLI license number, or use the file method below
    number = os.environ.get("CCLI_NUM")
    if number is None:
        with open (f'{scripts_folder}/ccli_license_number.txt') as l:
            number = l.read().strip()
    print(f"Warning: CCLI License number not found for {song_title}. Feel free to ignore this message if the song is in the public domain")
    return f"CCLI Licence No: {number}"
