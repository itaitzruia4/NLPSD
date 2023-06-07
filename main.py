import numpy as np
from typing import Dict
import pickle

from protocol_getter import ProtocolGetter
from warning_counter import WarningCounter
from agg_scores_rater import AggScoresRater
from consts import *


def main():
    category_ids = CATEGORY_IDS
    min_knesset_num, max_knesset_num = MIN_KNESSET_NUM, MAX_KNESSET_NUM
    
    protocol_getter = ProtocolGetter(COMMITTEES_PATH, min_knesset_num, max_knesset_num, category_ids)

    model = 'finetune'
    agg_scores_rater = AggScoresRater(model_path=f'model_{model}.pt')

    agg_scores = dict()
    warning_counter = WarningCounter(MEMBERS_PATH)
    warnings = dict()

    for committee_id in protocol_getter.committee_ids:
        protocols2paths: Dict[int, str] = protocol_getter.get_protocols_paths(committee_id)
        # print(f'fetched {len(protocols2paths)} protocols for category {committee_id}')
        
        for id in list(protocols2paths.keys()):
            if id in warnings:
                print(f'warning: protocol with id {id} already in warnings')
            
            # count warnings and rate aggressiveness of current protocol
            text = protocol_getter.get_meeting_protocol_text(protocols2paths[id])
            filtered_text = filter_protocol_sentences(text)

            if filtered_text is None:
                print(f'warning: skipping protocol with id {id}')
                del text
                del protocols2paths[id]
                protocols2paths[id] = None
                continue

            # print('analyzing protocol with id', id)
            
            warnings[id] = warning_counter.count_warnings(text)
            sentences = filtered_text.split('\n')
            score = agg_scores_rater.rate_aggressiveness(sentences)

            if id in agg_scores:
                print(f'warning: protocol with id {id} already in agg_scores')
            agg_scores[id] = score

        
            # clear memory to avoid memory leak
            del protocols2paths[id]
            protocols2paths[id] = None
            del text
            

        del protocols2paths
        protocols2paths = None

    # save results to pickle files
    with open(f'results/warnings_{model}.pkl', 'wb') as f:
        pickle.dump(warnings, f)

    with open(f'results/agg_scores_{model}.pkl', 'wb') as f:
        pickle.dump(agg_scores, f)

    total_warnings = warning_counter.total_warnings
    with open(f'results/total_warnings_{model}.pkl', 'wb') as f:
        pickle.dump(total_warnings, f)

    # print(f'average agg score for model {model}:', np.mean(list(agg_scores.values())))

    # top_warnings = sorted(total_warnings.items(), key=lambda x: sum(x[1]), reverse=True)[:10]

    # print('top warnings:')
    # for warn in top_warnings:
    #     print(warn)


if __name__ == '__main__':
    main()