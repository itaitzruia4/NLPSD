import numpy as np
from typing import Dict, List
import pickle
import sys

from protocol_getter import ProtocolGetter
from warning_counter import WarningCounter
from agg_scores_rater import AggScoresRater
from consts import *


def main():
    if len(sys.argv) < 3:
        print('usage: python main.py <knesset_num> <category_id>')
        return
    
    knesset_num = int(sys.argv[1])
    category_id = int(sys.argv[2])

    # category_ids = CATEGORY_IDS
    category_ids = [category_id]

    # min_knesset_num, max_knesset_num = MIN_KNESSET_NUM, MAX_KNESSET_NUM
    min_knesset_num, max_knesset_num = knesset_num, knesset_num
    
    protocol_getter = ProtocolGetter(COMMITTEES_PATH, min_knesset_num, max_knesset_num, category_ids)

    model = 'finetune'
    agg_scores_rater = AggScoresRater(model_path=f'model_{model}.pt')

    warning_counter = WarningCounter(MEMBERS_PATH)

    protocols2paths: Dict[int, str] = protocol_getter.get_protocols_paths(protocol_getter.committee_ids[0], limit=10)
    
    for id in list(protocols2paths.keys()):
        # count warnings and rate aggressiveness of current protocol
        text = protocol_getter.get_meeting_protocol_text(protocols2paths[id])
        filtered_text = filter_protocol_sentences(text)
        
        warnings: Dict[str, List[int]] = warning_counter.count_warnings(text)
        sentences = filtered_text.split('\n')
        agg_score = agg_scores_rater.rate_aggressiveness(sentences)

    results = {
        'warnings': warnings,
        'agg_score': agg_score
    }

    # save results to pickle files
    with open(f'results/{model}_{knesset_num}_{category_id}.pkl', 'wb') as f:
        pickle.dump(results, f)

    
if __name__ == '__main__':
    main()