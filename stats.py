from consts import *
import pandas as pd


class Statistics:
    def __init__(self, categories2committies):
        df = pd.read_csv('kns_csv_files/kns_committeesession.csv')
        df = df[df['KnessetNum'] >= MIN_KNESSET_NUM]

        data = dict.fromkeys(range(MIN_KNESSET_NUM, CURRENT_KNESSET_NUM + 1))
        for knesset_num in data:
            data[knesset_num] = dict.fromkeys(CATEGORY_IDS)
            for category_id in data[knesset_num]:
                data[knesset_num][category_id] = df[(df['KnessetNum'] == knesset_num) & (df['CommitteeID'].isin(categories2committies[category_id]))]['CommitteeSessionID'].to_list()

        print('all session ids:')
        print(data)