import re
from collections import Counter

# Committees category id's
MESADERET_COM_CATEGORY_ID = 689
KNESSET_COM_CATEGORY_ID = 1
MONEY_COM_CATEGORY_ID = 2
DEFENSE_COM_CATEGORY_ID = 4
LAW_ORDER_COM_CATEGORY_ID = 6
SCIENCE_COM_CATEGORY_ID = 13

COMMITTEES_PATH = "kns_csv_files/kns_committee.csv"
MEMBERS_PATH = "kns_csv_files/kns_person.csv"
MIN_KNESSET_NUM = 20
MAX_KNESSET_NUM = 25
CATEGORY_IDS = [
    MONEY_COM_CATEGORY_ID,
    DEFENSE_COM_CATEGORY_ID,
    LAW_ORDER_COM_CATEGORY_ID,
    MESADERET_COM_CATEGORY_ID,
    KNESSET_COM_CATEGORY_ID,
]

CATEGORY_ID_TO_NAME = {
    MONEY_COM_CATEGORY_ID: "finance",
    DEFENSE_COM_CATEGORY_ID: "defense",
    LAW_ORDER_COM_CATEGORY_ID: "law and order",
    KNESSET_COM_CATEGORY_ID: "knesset",
    SCIENCE_COM_CATEGORY_ID: "science",
}

_new_regex1 = '<< דובר >>.*\n\n.*\n\n.*יו"ר.*\n\n.*פעם ה?ראש'
_new_regex2 = '<< דובר >>.*\n\n.*\n\n.*יו"ר.*\n\n.*קריאה ה?ראש'
_new_regex3 = '<< דובר >>.*\n\n.*\n\n.*יו"ר.*\n\n.*פעם ה?שני'
_new_regex4 = '<< דובר >>.*\n\n.*\n\n.*יו"ר.*\n\n.*קריאה ה?שני'
_new_regex5 = '<< דובר >>.*\n\n.*\n\n.*יו"ר.*\n\n.*פעם ה?שליש'
_new_regex6 = '<< דובר >>.*\n\n.*\n\n.*יו"ר.*\n\n.*קריאה ה?שליש'
NEW_WARNING_REGEX = "|".join(
    [_new_regex1, _new_regex2, _new_regex3, _new_regex4, _new_regex5, _new_regex6]
)

_old_regex1 = '.*:\n\n.*\n\n.*יו"ר.*\n\n.*פעם ה?ראש'
_old_regex2 = '.*:\n\n.*\n\n.*יו"ר.*\n\n.*קריאה ה?ראש'
_old_regex3 = '.*:\n\n.*\n\n.*יו"ר.*\n\n.*פעם ה?שני'
_old_regex4 = '.*:\n\n.*\n\n.*יו"ר.*\n\n.*קריאה ה?שני'
_old_regex5 = '.*:\n\n.*\n\n.*יו"ר.*\n\n.*פעם ה?שליש'
_old_regex6 = '.*:\n\n.*\n\n.*יו"ר.*\n\n.*קריאה ה?שליש'
OLD_WARNING_REGEX = "|".join(
    [_old_regex1, _old_regex2, _old_regex3,_old_regex4, _old_regex5, _old_regex6]
)


def is_old_format(text):
    return re.search("<< יור >>") is None


def filter_protocol_sentences(text: str, old_format=False) -> str:
    pattern = 'היו"ר.*:' if old_format else "<< יור >>"
    ind = re.search(pattern, text)

    if ind is None:
        return None

    txt2 = text[ind.span()[0]:]
    txt2 = re.sub("<<.*", "", txt2)
    txt2 = re.sub(">>.*", "", txt2)
    txt2 = re.sub(".*:", "", txt2)
    txt2 = re.sub("-", " ", txt2)
    txt2 = re.sub("\n( )+", "\n", txt2)
    txt2 = re.sub(" +", " ", txt2)
    txt2 = re.sub("\t", "", txt2)
    return txt2


def get_speakers_info(txt, knesset_members):
    """
    returns:
    1) counter of Knesset members talking rights
    2) number of people got talking rights
    3) number of talking rights
    """

    findings = re.findall("<< דובר >>.+<< דובר >>", txt)
    findings_counter = Counter(findings)
    knesset_rights_counter = {}
    for name, number in findings_counter.items():
        for member in knesset_members:
            if member in name:
                knesset_rights_counter[member] = number
                break
    return knesset_rights_counter, len(findings_counter), len(findings)
