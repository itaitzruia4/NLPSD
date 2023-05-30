from typing import List
import pandas as pd
import requests

class ProtocolGetter:
    def __init__(self, comittees_path: str, min_knesset_num: int, category_ids: List[int]):
        df = pd.read_csv(comittees_path)
        df = df[['CommitteeID', 'CategoryID', 'KnessetNum']]
        df = df[df['KnessetNum'] >= min_knesset_num]
        df = df[df['CategoryID'].isin(category_ids)]

        commitee_ids = df['CommitteeID'].to_list()
        self.commitee_ids = commitee_ids

        self.categories2committies = {category_id: df[df['CategoryID'] == category_id]['CommitteeID'].to_list() for category_id in category_ids}

        self.meeting_protocol_base_url = 'https://production.oknesset.org/pipelines/data/committees/meeting_protocols_text/'

    def get_meeting_protocol_text(self, text_path: str) -> str:
        # Send GET request to the URL
        response = requests.get(self.meeting_protocol_base_url + text_path)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            response.encoding = 'utf-8'
            # Retrieve the content of the file
            return response.text
        else:
            raise ValueError(f"Failed to retrieve content. Status code: {response.status_code}")

    def get_meeting_protocols(self, committee_id) -> List[str]:
        com_session_df = pd.read_csv('kns_csv_files/kns_committeesession.csv')
        com_session_df = com_session_df[com_session_df['CommitteeID'] == committee_id]
        com_session_df.dropna(subset=['text_parsed_filename'], inplace=True)

        session_ids = com_session_df['CommitteeSessionID'].astype(int).to_list()
        text_paths = com_session_df['text_parsed_filename'].to_list()
        session_ids2texts = {id: self.get_meeting_protocol_text(path) for id, path in zip(session_ids, text_paths)}
        return session_ids2texts


    