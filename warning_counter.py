import re
import pandas as pd
from typing import List, Tuple
from copy import deepcopy
import utils


class WarningCounter:
    def __init__(self, members_file_path: str):
        knesset_members_df = pd.read_csv(members_file_path)
        first_names = knesset_members_df['FirstName'].to_list()
        last_names = knesset_members_df['LastName'].to_list()
        knesset_members = [' '.join([first_name, last_name])
                           for first_name, last_name
                           in zip(first_names, last_names)]

        self.warnings = {mem: [0, 0, 0] for mem in knesset_members}

        # handle members with a middle name or a nickname
        new_first_names, new_last_names = [], []

        for fn, ln in zip(first_names, last_names):
            names = fn.replace('-', ' ').split(' ')
            
            if len(names) == 1:
                continue
            for name in names:
                self.warnings[name + ' ' + ln] = self.warnings[fn + ' ' + ln]
                new_first_names.append(name)
                new_last_names.append(ln)

            # update first and last names
            first_names += new_first_names
            last_names += new_last_names

            self.knesset_members = [
                ' '.join([first_name, last_name])
                for first_name, last_name in zip(first_names, last_names)
            ]

    def count_warnings(self,
                       text,
                       old_format=False
                       ) -> Tuple[dict, int]:
        """
        Return warnings from the meeting protocol text.

        Parameters
        ----------
        text : str
            Meeting protocol text.

        warnings: Dict[str, List[int]]
            Number of warnings for each Knesset member.

        knesset_members: List[str]
            List of Knesset members.
        """
        word2idx = {'ראש': 0, 'שני': 1, 'שליש': 2}

        pattern = utils.OLD_WARNING_REGEX \
            if old_format \
            else utils.NEW_WARNING_REGEX

        # find all warnings
        matches = re.findall(pattern, text, flags=re.MULTILINE)
        for match in matches:
            sentences = match.split('\n')
            first_sentence, last_sentence = sentences[0], sentences[-1]
            found = False
            for kns_member in self.knesset_members:
                if found:
                    break
                if kns_member in first_sentence:
                    for word, idx in word2idx.items():
                        if word in last_sentence:
                            self.warnings[kns_member][idx] += 1
                            found = True
        del matches

        # keep a copy of the warnings
        result = deepcopy(self.warnings)
        
        # reset warnings
        for warnings in self.warnings.values():
            for idx in range(len(warnings)):
                warnings[idx] = 0
        
        return result
