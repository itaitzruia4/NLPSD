# Detection and Analysis of Aggressive Behavior in Knesset Committees
The final project for the Natural Language Processing and Social Dynamics course at Ben-Gurion University of the Negev, supervised by [Dr. Oren Tsur](https://www.naslab.ise.bgu.ac.il/orentsur).

## Introduction
This project aims to automatically detect warnings and removals in Knesset committee meetings, and evaluate the level of agression exhibited in these meetings. The project utilizes a combination of regular expression (regex) based warning detection and a fine-tuned [AlephBert](https://huggingface.co/onlplab/alephbert-base) model for agression scoring. 

## Data
The data used in this project consists of 2070 documented meeting protocols taken from Knesset 20 to Knesset 25, focusing on the following committees:
- Knesset Committee
- Finance Committee
- Defense Committee
- Law and Order Committee
- Science and Technology Committee.

The meeting protocols were obtained via GET requests from the [Open Knesset website](https://oknesset.org/).

## Warning Detection
Warning detection in the meeting protocols is performed using regular expressions (regex). The regex patterns are designed to identify specific warning phrases or keywords that are commonly used in the context of Knesset committee meetings. The code for warning detection can be found in the file `warning_counter.py`.

## Aggressiveness Scoring
The aggressiveness scoring is accomplished through a fine-tuned AlephBert model. The model has been pretrained on a large corpus of Hebrew text and further fine-tuned on a labeled dataset of aggressive language. The AlephBert model takes a text input and produces a score indicating the level of aggressiveness present in the text. The code for the aggressiveness scoring can be found in the file `agg_scores_rater.py`.

## Requirements
Before running the code or using the models, make sure you have the following dependencies installed:

- Python 3.6
- PyTorch
- Transformers (Hugging Face)
- Numpy
- Pandas

## Usage
Make sure you have the required dependencies installed as mentioned in the "Requirements" section.
Run the `main.py` script to perform the whole process.
For each meeting protocol, an appropriate pickle file will be located in the `results` folder.
Each file contains the following information:
- warnings: Dictionary of (Knesset Member, Warnings), where Warnings is a list of the number of first, second, and third warnings for the Knesset member in this meeting, respectfully.
- agg_score: Aggressiveness score given to this meeting by the AlephBert model.
- speaker_cnt: a Counter object that counts the number of times each Knesset member has spoken.
- n_speakers: Number of speakers in the meeting.
- n_speaks: Number of times someone spoke during the meeting (the length of the conversation).

## Disclaimer
Please note that the automatic detection of warnings and removals, as well as the evaluation of aggressiveness, might not be 100% accurate. Human review and validation of the results are recommended.

## Contact
If you have any questions or need further assistance with the project, feel free to create a discussion or submit an issue in this repository.
