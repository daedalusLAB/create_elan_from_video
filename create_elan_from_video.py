#!/usr/bin/env python3

import os
import argparse
import json
import pandas as pd
import csv
import pympi


# get current_path
current_path = os.getcwd()

def transcribe(filename, input_folder, output_folder):
    # create folder with the name of the video in the output folder
    os.system("mkdir " + output_folder + "/" + filename)
    # transcript with whisperX and save the output in output_folder/filename
    os.system("whisperx --model large --output_format all --output_dir " + output_folder + "/" + filename + " " + input_folder + "/" + filename)


def extract_timestamps(input_file, output_file):
    # Read the JSON file
    with open(input_file, 'r') as f:
        json_data = json.load(f)

    # Initialize an empty list to store the extracted data
    extracted_data = []
    
    # Initialize variables to store previous timestamps
    prev_start = 0.0
    prev_end = 0.0

    # Loop through each segment in the JSON data
    for segment in json_data['segments']:
        # Loop through each word in the segment
        for word_data in segment['words']:
            # Extract the word
            word = word_data['word']
            
            # Check if 'start' and 'end' keys exist
            if 'start' in word_data and 'end' in word_data:
                start = word_data['start']
                end = word_data['end']
                # Update previous timestamps
                prev_start = start
                prev_end = end
            else:
                # Use previous timestamps for words without their own timestamps
                start = prev_start
                end = prev_end
            
            # Append the data to the list
            #word = ''.join(e for e in word if e.isalnum())

            extracted_data.append([word, start, end])

    # Create a DataFrame from the list
    df = pd.DataFrame(extracted_data, columns=['Word', 'Start', 'End'])
    # delete last row
    df = df[:-1]
    
    # Save the DataFrame as a CSV file
    print('Input file: ' + input_file)
    print('Saving CSV file to ' + output_file)
    df.to_csv(output_file, index=False)


def create_eaf(path, video_file):
    elan = pympi.Elan.Eaf(author="Daedalus Lab - Raul Sacnhez <raul@um.es>")
    
    # add media file
    elan.add_linked_file(video_file, mimetype="video/mp4")


    elan.add_tier("Transcription")
    print('Adding annotations to ELAN file...')

    with open(path + '/words_aligned.csv', 'r') as csvfile:
        
        csv_reader = csv.reader(csvfile)
        next(csv_reader, None)  # Skip header row

        i = 0
        for row in csv_reader:
            # if row data is not empty
            if row:
                i += 1
                word, start_time, end_time = row
                start_time_ms = int(float(start_time) * 1000)
                end_time_ms = int(float(end_time) * 1000)
                if start_time_ms != end_time_ms:
                    elan.add_annotation("Transcription", start_time_ms, end_time_ms, word )

    # save elanf file to path + foldername + .eaf
    elan.to_file(path + '/' + path.split('/')[-1] + '.eaf')


if __name__ == '__main__':
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Generate EAF files from a folder of JSON files.')
    parser.add_argument('-i', '--input', type=str, help='Path to the input folder with the videos.')
    parser.add_argument('-o', '--output', type=str, help='Path to the output folder.')
    parser.add_argument('-j', '--jsonmode', type=bool, default=False, help='If true, no whisper transcription will be done and the input folder should contain the json files.')
    args = parser.parse_args()

    # if output folder does not exist create it
    if not os.path.exists(args.output):
        os.makedirs(args.output)

    # Loop over all .mp4 files in the folder
    for filename in os.listdir(args.input):
        if filename.endswith(".mp4"):
            print("Processing: " + filename)
            # if jsonmode is false, transcribe the video
            if not args.jsonmode:
                # transcribe the video
                transcribe(filename, args.input, args.output)
            # extract timestamps from 
            filename_no_extension = filename.replace(".mp4", "")
            extract_timestamps(args.output + "/" + filename + "/" + filename_no_extension + ".json", args.output + "/" + filename + "/words_aligned.csv")
            # create eaf file
            create_eaf(args.output + "/" + filename, args.input + "/" + filename)

