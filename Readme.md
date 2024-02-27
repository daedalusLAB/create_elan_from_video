# Video to ELAN Transcription


"Video to ELAN Transcription" is a Python script designed to transcribe video files into EAF files using the WhisperX tool. The script takes as input a directory containing video files and outputs transcriptions in the form of EAF files in a specified output directory.

The script works by iterating over all the .mp4 files in the input directory, transcribing each video, extracting timestamps, and creating an EAF file for each video. The transcription process is handled by the WhisperX tool, which is invoked via a system call within the script.

The resulting EAF files are created using the pympi library and contain annotations for each word spoken in the video, along with the start and end times for each word. These annotations are stored in a tier named "Transcription".

This project is ideal for researchers and developers who need to transcribe large amounts of video data into a format that can be easily analyzed and manipulated.

![elan](https://github.com/daedalusLAB/create_elan_from_video/assets/1314992/c879c168-3059-4d06-b1a5-f65db100ab39)

## Installation

Clone the repository and install the required packages. We suggest using a virtual environment to avoid conflicts with other packages.

```sh
conda create -n create_elan_from_video python=3.10
conda activate create_elan_from_video
```

and then

```sh
git clone https://github.com/daedalusLAB/create_elan_from_video.git
cd create_elan_from_video
pip install -r requirements.txt

```

## Usage

To use this script, you need to provide the input and output directories as command line arguments:

```sh
python create_elan_from_video.py --input path/to/input/videos --output path/to/output 
```
