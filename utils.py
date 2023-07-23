import re
from collections import Counter
from typing import List, Tuple, Dict

# Committees category IDs
KNESSET_COM_CATEGORY_ID = 1
MONEY_COM_CATEGORY_ID = 2
DEFENSE_COM_CATEGORY_ID = 4
LAW_ORDER_COM_CATEGORY_ID = 6
SCIENCE_COM_CATEGORY_ID = 13

# Knesset databases paths
COMMITTEES_PATH = "kns_csv_files/kns_committee.csv"
MEMBERS_PATH = "kns_csv_files/kns_person.csv"

# Knesset numbers
MIN_KNESSET_NUM = 20
MAX_KNESSET_NUM = 25

# Map category IDs to category names
CATEGORY_ID_TO_NAME = {
    MONEY_COM_CATEGORY_ID: "finance",
    DEFENSE_COM_CATEGORY_ID: "defense",
    LAW_ORDER_COM_CATEGORY_ID: "law and order",
    KNESSET_COM_CATEGORY_ID: "knesset",
    SCIENCE_COM_CATEGORY_ID: "science",
}

# Warning regex in new format
_new_regex1 = '<< דובר >>.*\n\n.*\n\n.*יו"ר.*\n\n.*פעם ה?ראש'
_new_regex2 = '<< דובר >>.*\n\n.*\n\n.*יו"ר.*\n\n.*קריאה ה?ראש'
_new_regex3 = '<< דובר >>.*\n\n.*\n\n.*יו"ר.*\n\n.*פעם ה?שני'
_new_regex4 = '<< דובר >>.*\n\n.*\n\n.*יו"ר.*\n\n.*קריאה ה?שני'
_new_regex5 = '<< דובר >>.*\n\n.*\n\n.*יו"ר.*\n\n.*פעם ה?שליש'
_new_regex6 = '<< דובר >>.*\n\n.*\n\n.*יו"ר.*\n\n.*קריאה ה?שליש'
NEW_WARNING_REGEX = "|".join(
    [_new_regex1, _new_regex2, _new_regex3,
     _new_regex4, _new_regex5, _new_regex6]
)

# Warning regex in new format
_old_regex1 = '.*:\n\n.*\n\n.*יו"ר.*\n\n.*פעם ה?ראש'
_old_regex2 = '.*:\n\n.*\n\n.*יו"ר.*\n\n.*קריאה ה?ראש'
_old_regex3 = '.*:\n\n.*\n\n.*יו"ר.*\n\n.*פעם ה?שני'
_old_regex4 = '.*:\n\n.*\n\n.*יו"ר.*\n\n.*קריאה ה?שני'
_old_regex5 = '.*:\n\n.*\n\n.*יו"ר.*\n\n.*פעם ה?שליש'
_old_regex6 = '.*:\n\n.*\n\n.*יו"ר.*\n\n.*קריאה ה?שליש'
OLD_WARNING_REGEX = "|".join(
    [_old_regex1, _old_regex2, _old_regex3,
     _old_regex4, _old_regex5, _old_regex6]
)


def is_old_format(text: str) -> bool:
    '''
    Checks if the text is in the old format

    Parameters:
    -----------
    text: str
        The text to check
    
    Returns:
    --------
    bool
        True if the text is in old format, False otherwise
    '''
    return re.search("<< יור >>", text) is None


def filter_protocol_sentences(text: str, old_format=False) -> str:
    '''
    Filters the protocol sentences from the text

    Parameters:
    -----------
    text: str
        The text to filter
    old_format: bool
        True if the text is in old format, False otherwise

    Returns:
    --------
    str
        The filtered text, containing sentences only
        with no speakers information
    '''
    pattern = 'היו"ר.*:' if old_format else "<< יור >>"
    ind = re.search(pattern, text)

    if ind is None:
        print('Warning: no chairman found')
    else:
        text = text[ind.span()[0]:]
        del ind

    text = re.sub("<<.*", "", text)
    text = re.sub(">>.*", "", text)
    text = re.sub(".*:", "", text)
    text = re.sub("-", " ", text)
    text = re.sub("\n( )+", "\n", text)
    text = re.sub(" +", " ", text)
    text = re.sub("\t", "", text)
    return text


def get_speakers_info(txt: str,
                      knesset_members: List[str],
                      old_format=False
                      ) -> Tuple[Counter, int, int]:
    '''
    Extracts speakers information from the text

    Parameters:
    -----------
    txt: str
        The text to extract speakers information from
    knesset_members: list
        A list of knesset members names
    old_format: bool
        True if the text is in old format, False otherwise
    
    Returns:
    --------
    Tuple[Dict[str, int], int, int]
        A tuple containing:
        1) A Counter mapping members names to number of times they spoke
        2) The number of speakers
        3) The number of speech instances in total
    '''
    # Find all instances of speakers
    if old_format:
        findings = re.findall(".*:", txt)
    else:
        findings = re.findall("<< דובר >>.+<< דובר >>", txt)
    findings_counter = Counter(findings)
    
    # Map knesset members names to number of times they spoke
    knesset_rights_counter = {}
    for name, number in findings_counter.items():
        for member in knesset_members:
            if member in name:
                knesset_rights_counter[member] = number
                break
    n_speaks = len(findings)
    n_speakers = len(findings_counter)
    del findings
    del findings_counter
    return knesset_rights_counter, n_speakers, n_speaks
