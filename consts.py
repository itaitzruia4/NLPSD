# Committee id's
MESADERET_24_COM_ID = 2215
KNESSET_24_COM_ID = 3991

MONEY_25_COM_ID = 4186
DEFENSE_25_COM_ID = 4190
LAW_ORDER_25_COM_ID = 4191

# Commities category id's
MESADERET_COM_CATEGORY_ID = 689
KNESSET_COM_CATEGORY_ID = 1
MONEY_COM_CATEGORY_ID = 2
DEFENSE_COM_CATEGORY_ID = 4
LAW_ORDER_COM_CATEGORY_ID = 6

COMMITTEES_PATH = 'kns_csv_files/kns_committee.csv'
MEMBERS_PATH = 'kns_csv_files/kns_person.csv'
MIN_KNESSET_NUM = 24
CURRENT_KNESSET_NUM = 25
CATEGORY_IDS = [MONEY_COM_CATEGORY_ID, DEFENSE_COM_CATEGORY_ID, LAW_ORDER_COM_CATEGORY_ID, MESADERET_COM_CATEGORY_ID, KNESSET_COM_CATEGORY_ID]

_regex1 = '<< דובר >>.*\n\n.*\n\n.*יו"ר.*\n\n.*פעם ה?ראש'
_regex2 = '<< דובר >>.*\n\n.*\n\n.*יו"ר.*\n\n.*קריאה ה?ראש'
_regex3 = '<< דובר >>.*\n\n.*\n\n.*יו"ר.*\n\n.*פעם ה?שני'
_regex4 = '<< דובר >>.*\n\n.*\n\n.*יו"ר.*\n\n.*קריאה ה?שני'
_regex5 = '<< דובר >>.*\n\n.*\n\n.*יו"ר.*\n\n.*פעם ה?שליש'
_regex6 = '<< דובר >>.*\n\n.*\n\n.*יו"ר.*\n\n.*קריאה ה?שליש'
WARNING_REGEX = '|'.join([_regex1, _regex2, _regex3, _regex4, _regex5, _regex6])

