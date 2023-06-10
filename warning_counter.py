import re
import pandas as pd
from typing import List, Tuple
from consts import WARNING_REGEX


class WarningCounter:
    def __init__(self, members_file_path: str):
        knesset_members_df = pd.read_csv(members_file_path)
        first_names, last_names = knesset_members_df['FirstName'].to_list(), knesset_members_df['LastName'].to_list()
        knesset_members = [' '.join([first_name, last_name]) for first_name, last_name in zip(first_names, last_names)]

        self.total_warnings = {mem: [0, 0, 0] for mem in knesset_members}

        # handle members with a middle name or a nickname
        new_first_names, new_last_names = [], []

        for fn, ln in zip(first_names, last_names):
            names = re.findall('\w+', fn)
            
            for name in names:
                self.total_warnings[name + ' ' + ln] = self.total_warnings[fn + ' ' + ln]
                new_first_names.append(name)
                new_last_names.append(ln)

        # update first and last names
        first_names = new_first_names
        last_names = new_last_names

        self.knesset_members = [' '.join([first_name, last_name]) for first_name, last_name in zip(first_names, last_names)]

    def count_warnings(self, text) -> Tuple[dict, int]:
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
        local_warnings = {mem: [0, 0, 0] for mem in self.knesset_members}
        word2idx = {'ראש': 0, 'שני': 1, 'שליש': 2}

        # find all warnings
        matches = re.findall(WARNING_REGEX, text, flags=re.MULTILINE)
        for match in matches:
            sentences = match.split('\n')
            first_sentence, last_sentence = sentences[0], sentences[-1]
            for kns_member in self.knesset_members:
                if kns_member in first_sentence:
                    for word, idx in word2idx.items():
                        if word in last_sentence:
                            self.total_warnings[kns_member][idx] += 1
                            local_warnings[kns_member][idx] += 1
                            break
        
        return local_warnings, len(matches)