from consts import *
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple


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

        self.knesset_categories_sessions = knesset_categories_sessions

        knesset_members_df = pd.read_csv(MEMBERS_PATH)
        first_names, last_names = knesset_members_df['FirstName'].to_list(), knesset_members_df['LastName'].to_list()
        self.knesset_members = [' '.join([first_name, last_name]) for first_name, last_name in zip(first_names, last_names)]

    #####################
    # Warnings Statistics 
    #####################
    def warnings_per_knesset_num(self, sessions2warnings) -> Dict[int, Dict[str, List[int]]]:
        '''
        Returns a dictionary of the form:
        {
            knesset_num:
            {
                member: 
                [
                    first_warnings,
                    second_warnings,
                    third_warnings
                ]
            }
        }
        '''
        warnings_per_knesset_nums = dict.fromkeys(self.knesset_categories_sessions)
        n_protocols_per_knesset_nums = dict.fromkeys(self.knesset_categories_sessions)
        for knesset_num in self.knesset_categories_sessions:
            warnings_per_knesset_nums[knesset_num] = dict.fromkeys(self.knesset_members)
            n_protocols_per_knesset_nums[knesset_num] = 0
            for category_id in self.knesset_categories_sessions[knesset_num]:
                n_protocols_per_knesset_nums[knesset_num] += len(self.knesset_categories_sessions[knesset_num][category_id])
                for committee_session_id in self.knesset_categories_sessions[knesset_num][category_id]:
                    # update warnings
                    warnings_filtered = {member: warnings for member, warnings in sessions2warnings[committee_session_id].items() if member in self.knesset_members}
                    for member, warnings in warnings_filtered.items():
                        if member not in warnings_per_knesset_nums[knesset_num]:
                            warnings_per_knesset_nums[knesset_num][member] = np.zeros(shape=3)
                        warnings_per_knesset_nums[knesset_num][member] += np.array(warnings)
        return warnings_per_knesset_nums, n_protocols_per_knesset_nums
    
    def warnings_per_category(self, sessions2warnings) -> Dict[str, Dict[str, List[int]]]:
        '''
        Returns a dictionary of the form:
        {
            category_id:
            {
                member: 
                [
                    first_warnings,
                    second_warnings,
                    third_warnings
                ]
            }
        }
        '''
        warnings_per_categories = dict.fromkeys(CATEGORY_IDS)
        n_protocols_per_categories = dict.fromkeys(CATEGORY_IDS)
        for category_id in warnings_per_categories:
            warnings_per_categories[category_id] = dict.fromkeys(self.knesset_members)
            n_protocols_per_categories[category_id] = 0
            for knesset_num in self.knesset_categories_sessions:
                n_protocols_per_categories[category_id] += len(self.knesset_categories_sessions[knesset_num][category_id])
                for committee_session_id in self.knesset_categories_sessions[knesset_num][category_id]:
                    # update warnings
                    warnings_filtered = {member: warnings for member, warnings in sessions2warnings[committee_session_id].items() if member in self.knesset_members}
                    for member, warnings in warnings_filtered.items():
                        if member not in warnings_per_categories[category_id]:
                            warnings_per_categories[category_id][member] = np.zeros(shape=3)
                        warnings_per_categories[category_id][member] += np.array(warnings)
        return warnings_per_categories, n_protocols_per_categories
    
    def warnings_per_committee(self, sessions2warnings) -> Dict[int, Dict[str, Dict[str, List[int]]]]:
        '''
        Returns a dictionary of the form:
        {
            knesset_num:
            {
                category_id:
                {
                    member: 
                    [
                        first_warnings,
                        second_warnings,
                        third_warnings
                    ]
                }
            }
        }
        '''
        warnings_per_committee = dict.fromkeys(self.knesset_categories_sessions)
        for knesset_num in self.knesset_categories_sessions:
            warnings_per_committee[knesset_num] = dict.fromkeys(self.knesset_categories_sessions[knesset_num])
            for category_id in warnings_per_committee[knesset_num]:
                warnings_per_committee[knesset_num][category_id] = dict.fromkeys(self.knesset_members)
                for committee_session_id in self.knesset_categories_sessions[knesset_num][category_id]:
                    # update warnings
                    warnings_filtered = {member: warnings for member, warnings in sessions2warnings[committee_session_id].items() if member in self.knesset_members}
                    for member, warnings in warnings_filtered.items():
                        if member not in warnings_per_committee[knesset_num][category_id]:
                            warnings_per_committee[knesset_num][category_id][member] = np.zeros(shape=3)
                        warnings_per_committee[knesset_num][category_id][member] += np.array(warnings)
        return warnings_per_committee
    
    def average_warnings_per_knesset_num(self,
                                         warnings_per_knesset_nums,
                                         n_protocols_per_knesset_nums) -> Dict[int, float]:
        '''
        Returns a dictionary of the form:
        {
            knesset_num: avg_warnings
        }
        '''
        avg_warnings_per_knesset_nums = dict.fromkeys(self.knesset_categories_sessions)
        for knesset_num in self.knesset_categories_sessions:
            avg_warnings_per_knesset_nums[knesset_num] = np.zeros(shape=3)
            for warnings in warnings_per_knesset_nums[knesset_num].values():
                avg_warnings_per_knesset_nums[knesset_num] += warnings
            avg_warnings_per_knesset_nums[knesset_num] /= n_protocols_per_knesset_nums[knesset_num]

        return avg_warnings_per_knesset_nums

    
    #######################
    # Agg Scores Statistics 
    #######################
    def agg_scores_per_knesset_num(self, agg_scores) -> Dict[int, float]:
        '''
        Returns two dictionaries of the form:
        {
            knesset_num: agg_score
        }
        {
            knesset_num: n_protocols
        }
        '''
        n_protocols_per_knesset_nums = dict.fromkeys(self.knesset_categories_sessions)
        agg_scores_per_knesset_nums = dict.fromkeys(self.knesset_categories_sessions)
        for knesset_num in self.knesset_categories_sessions:
            curr_agg_scores = []
            for category_id in self.knesset_categories_sessions[knesset_num]:
                curr_agg_scores += [
                    agg_scores[committee_session_id] 
                    for committee_session_id in self.knesset_categories_sessions[knesset_num][category_id]
                ]
            agg_scores_per_knesset_nums[knesset_num] = np.mean(curr_agg_scores)
            n_protocols_per_knesset_nums[knesset_num] = len(curr_agg_scores)
        return agg_scores_per_knesset_nums, n_protocols_per_knesset_nums
    
    def agg_scores_per_category(self, agg_scores) -> Dict[int, float]:
        '''
        Returns two dictionaries of the form:
        {
            category_id: agg_score
        }
        {
            category_id: n_protocols
        }
        '''
        n_protocols_per_categories = dict.fromkeys(CATEGORY_IDS)
        agg_scores_per_categories = dict.fromkeys(CATEGORY_IDS)
        for category_id in CATEGORY_IDS:
            curr_agg_scores = []
            for knesset_num in self.knesset_categories_sessions:
                curr_agg_scores += [
                    agg_scores[committee_session_id] 
                    for committee_session_id in self.knesset_categories_sessions[knesset_num][category_id]
                ]
            agg_scores_per_categories[category_id] = np.mean(curr_agg_scores)
            n_protocols_per_categories[category_id] = len(curr_agg_scores)
        return agg_scores_per_categories, n_protocols_per_categories
    
    def agg_scores_per_committee(self, agg_scores) -> Dict[int, Dict[int, float]]:
        scores_per_knesset_nums_per_categories = dict.fromkeys(self.knesset_categories_sessions)
        for knesset_num in self.knesset_categories_sessions:
            scores_per_knesset_nums_per_categories[knesset_num] = dict.fromkeys(self.knesset_categories_sessions[knesset_num])
            for category_id in scores_per_knesset_nums_per_categories[knesset_num]:
                curr_scores = [
                    agg_scores[committee_session_id]
                    for committee_session_id
                    in self.knesset_categories_sessions[knesset_num][category_id]
                ]
                scores_per_knesset_nums_per_categories[knesset_num][category_id] = np.mean(curr_scores)
        return scores_per_knesset_nums_per_categories
    
    #######################

    
