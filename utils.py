import re
from collections import Counter

# Committees category id's
MESADERET_COM_CATEGORY_ID = 689
KNESSET_COM_CATEGORY_ID = 1
MONEY_COM_CATEGORY_ID = 2
DEFENSE_COM_CATEGORY_ID = 4
LAW_ORDER_COM_CATEGORY_ID = 6
SCIENCE_COM_CATEGORY_ID = 13

COMMITTEES_PATH = 'kns_csv_files/kns_committee.csv'
MEMBERS_PATH = 'kns_csv_files/kns_person.csv'
MIN_KNESSET_NUM = 20
MAX_KNESSET_NUM = 25
CATEGORY_IDS = [MONEY_COM_CATEGORY_ID,
                DEFENSE_COM_CATEGORY_ID,
                LAW_ORDER_COM_CATEGORY_ID,
                MESADERET_COM_CATEGORY_ID,
                KNESSET_COM_CATEGORY_ID]

CATEGORY_ID_TO_NAME = {
    MONEY_COM_CATEGORY_ID: 'finance',
    DEFENSE_COM_CATEGORY_ID: 'defense',
    LAW_ORDER_COM_CATEGORY_ID: 'law and order',
    KNESSET_COM_CATEGORY_ID: 'knesset',
    SCIENCE_COM_CATEGORY_ID: 'science'
}

_regex1 = '<< דובר >>.*\n\n.*\n\n.*יו"ר.*\n\n.*פעם ה?ראש'
_regex2 = '<< דובר >>.*\n\n.*\n\n.*יו"ר.*\n\n.*קריאה ה?ראש'
_regex3 = '<< דובר >>.*\n\n.*\n\n.*יו"ר.*\n\n.*פעם ה?שני'
_regex4 = '<< דובר >>.*\n\n.*\n\n.*יו"ר.*\n\n.*קריאה ה?שני'
_regex5 = '<< דובר >>.*\n\n.*\n\n.*יו"ר.*\n\n.*פעם ה?שליש'
_regex6 = '<< דובר >>.*\n\n.*\n\n.*יו"ר.*\n\n.*קריאה ה?שליש'
WARNING_REGEX = '|'.join([_regex1, _regex2, _regex3, _regex4, _regex5, _regex6])


def filter_protocol_sentences(text: str) -> str:
    ind = re.search("<< יור >>", text)

    if ind is None:
        return None

    txt2 = text[ind.span()[0]:]
    txt2 = re.sub("<<.*","", txt2)
    txt2 = re.sub(">>.*","", txt2)
    txt2 = re.sub(".*:","", txt2)
    txt2 = re.sub("-", " ", txt2)
    txt2 = re.sub("\n\s+","\n", txt2)
    txt2 = re.sub(" +"," ", txt2)
    txt2 = re.sub("\t","", txt2)
    return txt2

def get_speakers_info(txt, knesset_members, old_format= False):
  '''
  returns:
  1) counter of Knesset members talking rights
  2) number of people got talking rights
  3) number of talking rights
  '''
  if old_format:
     findings = re.findall(".*:", txt)
  else:
    findings = re.findall("<< דובר >>.+<< דובר >>", txt)
  findings_counter = Counter(findings)
  knesset_rights_counter = {}
  for name, number in findings_counter.items():
    for member in knesset_members:
      if member in name:
        knesset_rights_counter[member] = number
        break
  return knesset_rights_counter, len(findings_counter), len(findings)
