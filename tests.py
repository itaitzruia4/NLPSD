import pytest
import utils
from warning_counter import WarningCounter


class Tests:
    def test_middle_names(self):
        warning_counter = WarningCounter(utils.MEMBERS_PATH)
        full_name = 'מכלוף מיקי זוהר'
        nicknames = ['מיקי זוהר', 'מכלוף זוהר']

        warnings = warning_counter.warnings

        assert warnings[full_name] == [0, 0, 0]
        assert warnings[full_name] is warnings[nicknames[0]]
        assert warnings[full_name] is warnings[nicknames[1]]
        assert warnings[full_name] == warnings[nicknames[0]]
        assert warnings[full_name] == warnings[nicknames[1]]

    def test_middle_name_count_warnings(self):
        text = '''
<< דובר >> מכלוף מיקי זוהר (הליכוד): << דובר >>   

לא, לא מכובד. 

 << יור >> היו"ר בועז טופורובסקי: << יור >>   

חבר הכנסת מיקי זוהר, אני קורא אותך לסדר פעם ראשונה. אני מנסה לעשות דיון, זה לא עוזר כשצועקים. 
'''
        warning_counter = WarningCounter(utils.MEMBERS_PATH)
        warnings = warning_counter.count_warnings(text)
        full_name = 'מכלוף מיקי זוהר'
        nicknames = ['מיקי זוהר', 'מכלוף זוהר']

        assert warnings[full_name] == [1, 0, 0]
        assert warnings[full_name] is warnings[nicknames[0]]
        assert warnings[full_name] is warnings[nicknames[1]]
        assert warnings[full_name] == warnings[nicknames[0]]
        assert warnings[full_name] == warnings[nicknames[1]]

        wc_warnings = warning_counter.warnings
        assert wc_warnings[full_name] == [0, 0, 0]
        assert wc_warnings[full_name] is wc_warnings[nicknames[0]]
        assert wc_warnings[full_name] is wc_warnings[nicknames[1]]
        assert wc_warnings[full_name] == wc_warnings[nicknames[0]]
        assert wc_warnings[full_name] == wc_warnings[nicknames[1]]

    def test_count_warnings_old_format(self):
        text = '''
אורי מקלב:

משפט שיוביל לקריאה ראשונה.

היו"ר ניסן סלומינסקי:

חבר הכנסת אורי מקלב, אני קורא אותך לסדר פעם ראשונה.
'''
        warning_counter = WarningCounter(utils.MEMBERS_PATH)
        warnings = warning_counter.count_warnings(text, old_format=True)

        name = 'אורי מקלב'

        assert warnings[name] == [1, 0, 0]

        wc_warnings = warning_counter.warnings
        assert wc_warnings[name] == [0, 0, 0]
