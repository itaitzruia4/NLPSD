import pickle
import sys

from protocol_getter import ProtocolGetter
from warning_counter import WarningCounter
from agg_scores_rater import AggScoresRater
import utils


def main():
    if len(sys.argv) < 3:
        print('usage: python main.py <knesset_num> <category_id> <protocol_start_idx>?')
        return
    
    # Knesset number (20-25) and category id (1, 2, 4, 6, 13)
    knesset_num = int(sys.argv[1])
    category_id = int(sys.argv[2])

    # default: start processing the first protocol
    protocol_start_idx = 0
    if len(sys.argv) == 3:
        protocol_start_idx = int(sys.argv[3])

    category_ids = [category_id]
    protocol_getter = ProtocolGetter(utils.COMMITTEES_PATH,
                                     knesset_num,
                                     knesset_num,
                                     category_ids)

    model = 'finetune'
    agg_scores_rater = AggScoresRater(model_path=f'model_{model}.pt')
    warning_counter = WarningCounter(utils.MEMBERS_PATH)

    # Committee ID: unique identifier for a committee in a certain knesset
    committee_id = protocol_getter.committee_ids[0]
    print('committee id:', committee_id)

    # fetch protocols from the Knesset website
    # protocols2paths: dictionary of <session id, text protocol path>
    protocols2paths = protocol_getter.get_protocols_paths(committee_id,
                                                          start=protocol_start_idx)
    print(f'fetched {len(protocols2paths)} protocols)')

    for session_id in list(protocols2paths.keys()):
        # count warnings and rate aggressiveness of current protocol
        text = protocol_getter.get_meeting_protocol_text(protocols2paths[session_id])
        del protocols2paths[session_id]

        # whether we should parse the protocol in the old format
        old_format = utils.is_old_format(text)

        # extract speakers info from the protocol
        speaker_cnt, n_speakers, n_speaks = utils.get_speakers_info(
            text,
            warning_counter.knesset_members,
            old_format=old_format
        )

        # count warnings and filter protocol to sentences only
        warnings = warning_counter.count_warnings(text, old_format)
        filtered_text = utils.filter_protocol_sentences(text, old_format)
        del text

        lines = filtered_text.split('\n')
        sentences = []
        for line in lines:
            sentences.extend(line.split('.'))
        sentences = [s.strip() for s in sentences]
        del filtered_text
        
        # rate aggressiveness of the protocol
        agg_score = agg_scores_rater.rate_aggressiveness(sentences)
        del sentences

        # save results to pickle files
        results = {
            'warnings': warnings,
            'speaker_cnt': speaker_cnt,
            'n_speakers': n_speakers,
            'n_speaks': n_speaks,
            'agg_score': agg_score
        }

        with open(f'results/{model}_{session_id}.pkl', 'wb') as f:
            pickle.dump(results, f)
    
        # clear memory to avoid memory leaks
        del warnings
        del agg_score
        del speaker_cnt
        del results


if __name__ == '__main__':
    main()
