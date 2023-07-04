import numpy as np
from typing import Dict
import pickle
import sys

from protocol_getter import ProtocolGetter
from warning_counter import WarningCounter
from agg_scores_rater import AggScoresRater
import utils


def main():
    if len(sys.argv) < 3:
        print('usage: python main.py <knesset_num> <category_id> <protocol_start_idx>')
        return
    
    knesset_num = int(sys.argv[1])
    category_id = int(sys.argv[2])
    protocol_start_idx = int(sys.argv[3])

    # category_ids = CATEGORY_IDS
    category_ids = [category_id]

    # min_knesset_num, max_knesset_num = MIN_KNESSET_NUM, MAX_KNESSET_NUM
    min_knesset_num, max_knesset_num = knesset_num, knesset_num
    
    protocol_getter = ProtocolGetter(utils.COMMITTEES_PATH,
                                     min_knesset_num,
                                     max_knesset_num,
                                     category_ids)

    model = 'finetune'
    agg_scores_rater = AggScoresRater(model_path=f'model_{model}.pt')
    warning_counter = WarningCounter(utils.MEMBERS_PATH)

    committee_id = protocol_getter.committee_ids[0]
    print('committee id:', committee_id)
    protocols2paths: Dict[int, str] = protocol_getter.get_protocols_paths(committee_id, start=protocol_start_idx)
    print(f'fetched {len(protocols2paths)} protocols)')

    for session_id in list(protocols2paths.keys()):
        # count warnings and rate aggressiveness of current protocol
        text = protocol_getter.get_meeting_protocol_text(protocols2paths[session_id])
        del protocols2paths[session_id]

        speaker_cnt, n_speakers, n_speaks = utils.get_speakers_info(text, warning_counter.knesset_members)

        warnings, n_warnings = warning_counter.count_warnings(text)
        filtered_text = utils.filter_protocol_sentences(text)
        del text

        if filtered_text is None:
            print(f'warning: skipping protocol with id {session_id}')
            continue

        lines = filtered_text.split('\n')
        sentences = []
        for line in lines:
            sentences.extend(line.split('.'))
        sentences = [s.strip() for s in sentences if s.strip()]

        del filtered_text
        agg_score = agg_scores_rater.rate_aggressiveness(sentences)
        del sentences

        results = {
            'warnings': warnings,
            'speaker_cnt': speaker_cnt,
            'n_speakers': n_speakers,
            'n_speaks': n_speaks,
            'n_warnings': n_warnings,
            'agg_score': agg_score
        }

        # save results to pickle files
        with open(f'results/{model}_{session_id}.pkl', 'wb') as f:
            pickle.dump(results, f)
    
        # clear memory to avoid memory leak
        del warnings
        del n_warnings
        del agg_score
        del speaker_cnt
        del n_speakers
        del n_speaks


if __name__ == '__main__':
    main()
