import re
import numpy as np
from typing import Dict
import pickle
import requests

from protocol_getter import ProtocolGetter
from warning_counter import WarningCounter
from agg_scores_rater import AggScoresRater
from consts import *


def main():
    category_ids = CATEGORY_IDS
    min_knesset_num, max_knesset_num = 21, 21
    
    protocol_getter = ProtocolGetter(COMMITTEES_PATH, min_knesset_num, max_knesset_num, category_ids)

    model = 'finetune'
    # agg_scores_rater = AggScoresRater(model_path=f'model_{model}.pt')

    # agg_scores = dict()
    # warning_counter = WarningCounter(MEMBERS_PATH)
    # warnings = dict()

    for category_id in category_ids:
        protocols: Dict[int, str] = protocol_getter.get_meeting_protocols(category_id, limit=1)
        for session_id in protocols:
            with open(f'protocols/{session_id}.txt', 'w', encoding='utf-8') as f:
                f.write(protocols[session_id])

def filter_protocol_sentences(text: str) -> str:
    ind = re.search("<< יור >>", text)

    if ind is None:
        ind = re.search("יו\"ר.*:", text)
    txt2 = text[ind.span()[0]:]
    txt2 = re.sub("<<.*","", txt2)
    txt2 = re.sub(">>.*","", txt2)
    txt2 = re.sub(".*:","", txt2)
    txt2 = re.sub("-", " ", txt2)
    txt2 = re.sub("\n\s+","\n", txt2)
    txt2 = re.sub(" +"," ", txt2)
    txt2 = re.sub("\t","", txt2)
    return txt2

def get_meeting_protocol_text(text_path: str) -> str:
    # Send GET request to the URL
    meeting_protocol_base_url = 'https://production.oknesset.org/pipelines/data/committees/meeting_protocols_text/'
    response = requests.get(meeting_protocol_base_url + text_path)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        response.encoding = 'utf-8'
        # Retrieve the content of the file
        return response.text
    else:
        raise ValueError(f"Failed to retrieve content. Status code: {response.status_code}")
        
        
if __name__ == '__main__':
    # main()
    protocol_id = 2200827
    with open(f'protocols/{protocol_id}.txt', 'r', encoding='utf-8') as f:
        text = f.read()
    filtered_text = filter_protocol_sentences(text)
    with open(f'filtered_protocols/{protocol_id}.txt', 'w', encoding='utf-8') as f:
        f.write(filtered_text)