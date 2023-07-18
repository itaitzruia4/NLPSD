import sys
import os

import utils
from protocol_getter import ProtocolGetter


def main():
    if len(sys.argv) < 3:
        print('usage: python main.py <knesset_num> <category_id> <protocol_start_idx> <max_split_size>')
        return
    
    knesset_num = int(sys.argv[1])
    category_id = int(sys.argv[2])

    category_ids = [category_id]

    min_knesset_num, max_knesset_num = knesset_num, knesset_num
    
    protocol_getter = ProtocolGetter(utils.COMMITTEES_PATH,
                                     min_knesset_num,
                                     max_knesset_num,
                                     category_ids)

    model = 'finetune'
    committee_id = protocol_getter.committee_ids[0]
    
    protocols2paths = protocol_getter.get_protocols_paths(committee_id)
    missing = False
    for idx, session_id in enumerate(list(protocols2paths.keys())):
        if not os.path.exists(f'results/{model}_{session_id}.pkl'):
            print(f'Index {idx} missing')
            missing = True
    
    if not missing:
        print('All files exist! :D')


if __name__ == '__main__':
    main()
