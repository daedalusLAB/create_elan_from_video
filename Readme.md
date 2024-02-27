# Video to ELAN Transcription

This project is a Python script that transcribes video files to EAF files using the WhisperX tool.

![elan](https://github.com/daedalusLAB/create_elan_from_video/assets/1314992/c879c168-3059-4d06-b1a5-f65db100ab39)


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Installation

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
