import numpy as np

from protocol_getter import ProtocolGetter
from warning_counter import WarningCounter
from agg_scores_rater import AggScoresRater
from stats import Statistics
from typing import Dict

from consts import *


def main():
    protocol_getter = ProtocolGetter(COMMITTEES_PATH, MIN_KNESSET_NUM, CATEGORY_IDS)
    # statistics = Statistics(protocol_getter.categories2committies)

    model = 'transfer'
    if model == 'transfer':
        agg_scores_rater = AggScoresRater(model_path='model_transfer.pt')
    elif model == 'finetune':
        agg_scores_rater = AggScoresRater(model_path='model_finetune.pt')

    agg_scores = []
    warning_counter = WarningCounter(MEMBERS_PATH)

    for committee_id in protocol_getter.commitee_ids:
        protocols: Dict[int, str] = protocol_getter.get_meeting_protocols(committee_id)
        
        # warnings = {id: warning_counter.count_warnings(protocol) for id, protocol in protocols.items()}
        for protocol in protocols.values():
            warning_counter.count_warnings(protocol)
            score = agg_scores_rater.rate_aggressiveness(protocol)
            agg_scores.append(score)
        
    total_warnings = warning_counter.warnings
    top_warnings = sorted(total_warnings.items(), key=lambda x: sum(x[1]), reverse=True)[:10]

    print('top warnings:')
    for warn in top_warnings:
        print(warn)

    print(f'average agg score for model {model}:', np.mean(agg_scores))


if __name__ == '__main__':
    main()