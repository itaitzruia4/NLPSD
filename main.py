import numpy as np
import pandas as pd
import requests
import re

from collections import Counter
from typing import List, Dict

import torch
import torch.nn as nn

from consts import *

def main():
    df = pd.read_csv('kns_csv_files/kns_committee.csv')
    df = df[df['KnessetNum'] >= 25]
    df = df[df['CategoryID'].isin([MONEY_COM_CATEGORY_ID, DEFENSE_COM_CATEGORY_ID, LAW_ORDER_COM_CATEGORY_ID, MESADERET_COM_CATEGORY_ID, KNESSET_COM_CATEGORY_ID])]
    commitee_ids = df['CommitteeID'].to_list()

if __name__ == '__main__':
    main()