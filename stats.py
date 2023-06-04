from consts import *
import pandas as pd


class Statistics:
    def __init__(self):
        df = pd.read_csv(COMMITTEES_PATH)
        df = df[['CommitteeID', 'CategoryID', 'KnessetNum']]
        df = df[df['KnessetNum'] >= MIN_KNESSET_NUM]
        df = df[df['CategoryID'].isin(CATEGORY_IDS)]

        categories2committees = {category_id: df[df['CategoryID'] == category_id]['CommitteeID'].to_list() for category_id in CATEGORY_IDS}

        committee_session_df = pd.read_csv('kns_csv_files/kns_committeesession.csv')
        committee_session_df = committee_session_df[committee_session_df['KnessetNum'] >= MIN_KNESSET_NUM]

        knesset_categories_sessions = dict.fromkeys(range(MIN_KNESSET_NUM, CURRENT_KNESSET_NUM + 1))
        for knesset_num in knesset_categories_sessions:
            knesset_categories_sessions[knesset_num] = dict.fromkeys(CATEGORY_IDS)
            for category_id in knesset_categories_sessions[knesset_num]:
                knesset_categories_sessions[knesset_num][category_id] = committee_session_df[(committee_session_df['KnessetNum'] == knesset_num) & (committee_session_df['CommitteeID'].isin(categories2committees[category_id]))]['CommitteeSessionID'].to_list()

        