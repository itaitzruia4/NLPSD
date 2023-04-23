LAW_ORDER_25_DISCUSSION_IDS = [2200827]
MONEY_25_DISCUSSION_IDS = []
DEFENSE_25_DISCUSSION_IDS = []

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

CURRENT_KNESET_NUM = 25

_regex1 = '<< דובר >>.\n\n.\n\n.יו"ר.\n\n.*פעם ה?ראש'
_regex2 = '<< דובר >>.\n\n.\n\n.יו"ר.\n\n.*קריאה ה?ראש'
_regex3 = '<< דובר >>.\n\n.\n\n.יו"ר.\n\n.*פעם ה?שני'
_regex4 = '<< דובר >>.\n\n.\n\n.יו"ר.\n\n.*קריאה ה?שני'
_regex5 = '<< דובר >>.\n\n.\n\n.יו"ר.\n\n.*פעם ה?שליש'
_regex6 = '<< דובר >>.\n\n.\n\n.יו"ר.\n\n.*קריאה ה?שליש'
WARNING_REGEX = '|'.join([_regex1, _regex2, _regex3, _regex4, _regex5, _regex6])

rex4 = '<< דובר >>.*\n\n.*\n\n.*יו"ר.*\n\n.*פעם ה?ראש'
rex5 = '<< דובר >>.*\n\n.*\n\n.*יו"ר.*\n\n.*קריאה ה?ראש'
rex6 = '<< דובר >>.*\n\n.*\n\n.*יו"ר.*\n\n.*פעם ה?שני'
rex7 = '<< דובר >>.*\n\n.*\n\n.*יו"ר.*\n\n.*קריאה ה?שני'
rex8 = '<< דובר >>.*\n\n.*\n\n.*יו"ר.*\n\n.*פעם ה?שליש'
rex9 = '<< דובר >>.*\n\n.*\n\n.*יו"ר.*\n\n.*קריאה ה?שליש'
rex = '|'.join([rex4, rex5, rex6, rex7, rex8, rex9])