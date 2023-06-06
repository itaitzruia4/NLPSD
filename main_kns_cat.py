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
    if model == 'transfer':
        agg_scores_rater = AggScoresRater(model_path='model_transfer.pt')
    elif model == 'finetune':
        agg_scores_rater = AggScoresRater(model_path='model_finetune.pt')

    agg_scores = dict()
    warning_counter = WarningCounter(MEMBERS_PATH)
    warnings = dict()

    for committee_id in protocol_getter.committee_ids:
        protocols: Dict[int, str] = protocol_getter.get_meeting_protocols(committee_id, limit=10)
        
        # warnings = {id: warning_counter.count_warnings(protocol) for id, protocol in protocols.items()}
        for id, text in protocols.items():
            if id in warnings:
                print(f'warning: protocol with id {id} already in warnings')
            warnings[id] = warning_counter.count_warnings(text)
            score = agg_scores_rater.rate_aggressiveness(text)
            if id in agg_scores:
                print(f'warning: protocol with id {id} already in agg_scores')
            agg_scores[id] = score

            protocols[id] = None
            del text

        del protocols
        
        total_warnings = warning_counter.total_warnings
        # top_warnings = sorted(total_warnings.items(), key=lambda x: sum(x[1]), reverse=True)[:10]

        # print('top warnings:')
        # for warn in top_warnings:
        #     print(warn)

        print(f'average agg score for model {model}:', np.mean(list(agg_scores.items())))

        with open(f'results/agg_scores_{model}_{knesset_num}_{category_id}.pkl', 'wb') as f:
            pickle.dump(agg_scores, f)

        with open(f'results/total_warnings_{model}_{knesset_num}_{category_id}.pkl', 'wb') as f:
            pickle.dump(total_warnings, f)

        with open(f'results/warnings_{model}_{knesset_num}_{category_id}.pkl', 'wb') as f:
            pickle.dump(warnings, f)


if __name__ == '__main__':
    main()