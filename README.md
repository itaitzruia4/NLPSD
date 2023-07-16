# Automatic Detection of Warnings and Removals in Knesset Committee Meetings
The final project for the Natural Language Processing and Social Dynamics course at the Ben-Gurion University of the Negev,
supervised by [Dr. Oren Tsur](https://www.naslab.ise.bgu.ac.il/orentsur).

## Introduction
This project aims to automatically detect warnings and removals in Knesset committee meetings, and evaluate the level of aggressiveness exhibited in these meetings. The project utilizes a combination of regular expression (regex) based warning detection and a fine-tuned [AlephBert](https://huggingface.co/onlplab/alephbert-base) model for aggressiveness scoring. The data used in this project consists of 1653 meeting protocols from Knesset 20 to Knesset 25, focusing on the following committees: Knesset Committee, Finance Committee, Defense Committee, Law and Order Committee, and Science and Technology Committee.

## Requirements
Before running the code or using the models, make sure you have the following dependencies installed:

- Python 3.6
- PyTorch
- Transformers (Hugging Face)
- Numpy
- Pandas
- Requests
  
## Data
The dataset used in this project contains 1653 meeting protocols from Knesset 20 to Knesset 25. Each protocol represents a meeting from one of the specified committees: Knesset Committee, Finance Committee, Defense Committee, Law and Order Committee, or Science and Technology Committee. The meeting protocols were obtained via GET requests from the Open Knesset website.

## Warning Detection
Warning detection in the meeting protocols is performed using regular expressions (regex). The regex patterns are designed to identify specific warning phrases or keywords that are commonly used in the context of Knesset committee meetings. The code for warning detection can be found in the warning_detection.py file.

## Aggressiveness Scoring
The aggressiveness scoring is accomplished through a fine-tuned AlephBert model. The model has been pretrained on a large corpus of Hebrew text and further fine-tuned on a labeled dataset of aggressive language. The AlephBert model takes a text input and produces a score indicating the level of aggressiveness present in the text. The code for the aggressiveness scoring can be found in the aggressiveness_scoring.py file.

## Usage
Make sure you have the required dependencies installed as mentioned in the "Requirements" section.
Run the `main.py` script to perform the whole process.
For each meeting protocol, an appropriate pickle file will be located in the `results` folder.
Each file contains the following information:
- warnings: Dictionary of (Knesset Member, Warnings), where Warnings is a list of the number of first, second and third warnings for the Knesset member in this meeting, respectfully.
- agg_score: Aggressiveness score given to this meeting by the AlephBert model.
- speaker_cnt: a Counter object that counts the number of times each Knesset member has spoken.
- n_speakers: Number of speakers in the meeting.
- n_speaks: Number of times someone spoke during the meeting (the length of the conversation).

## Disclaimer
Please note that the automatic detection of warnings and removals, as well as the evaluation of aggressiveness, might not be 100% accurate. Human review and validation of the results are recommended.

## Contact
If you have any questions or need further assistance with the project, feel free to reach out to us via email: [Itai Tzruia - itaitz@post.bgu.ac.il, Ely Katz - elyk@post.bgu.ac.il].
