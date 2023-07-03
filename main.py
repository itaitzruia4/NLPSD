import numpy as np
from typing import Dict
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

    for committee_id in protocol_getter.committee_ids:
        protocols2paths: Dict[int, str] = protocol_getter.get_protocols_paths(committee_id)
        
        for session_id in list(protocols2paths.keys()):
            # count warnings and rate aggressiveness of current protocol
            text = protocol_getter.get_meeting_protocol_text(protocols2paths[session_id])
            del protocols2paths[session_id]
            protocols2paths[session_id] = None

            filtered_text = filter_protocol_sentences(text)

            if filtered_text is None:
                print(f'warning: skipping protocol with id {session_id}')
                continue

            
            warnings = warning_counter.count_warnings(text)
            del text
            sentences = filtered_text.split('\n')
            del filtered_text
            agg_score = agg_scores_rater.rate_aggressiveness(sentences)
            del sentences

            results = {
                'warnings': warnings,
                'agg_score': agg_score
            }

            # save results to pickle files
            with open(f'results/{model}_{session_id}.pkl', 'wb') as f:
                pickle.dump(results, f)
        
            # clear memory to avoid memory leak
            del warnings
            del agg_score
            

        del protocols2paths
        protocols2paths = None


    # print(f'average agg score for model {model}:', np.mean(list(agg_scores.values())))

    # top_warnings = sorted(total_warnings.items(), key=lambda x: sum(x[1]), reverse=True)[:10]

    # print('top warnings:')
    # for warn in top_warnings:
    #     print(warn)


if __name__ == '__main__':
    main()