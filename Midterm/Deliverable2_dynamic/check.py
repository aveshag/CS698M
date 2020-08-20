
# This program extract all signatures and later I used them as features
# This program also extract possible fields in summary

import sys
import os
import numpy as np
import glob
from os import listdir
from collections import Counter
import json


filename_list = glob.glob('Benign/*')
filename_list += glob.glob('Malware/*/*')
# print(filename_list)




summary = set()

# signature = set()
for en, file in enumerate(filename_list):
#     print(en)
    if en == 200:
        break
#     print(str(en) + ":")
    with open(file, 'r') as f:
        json_data = json.load(f)
        
        try:
            summary.update(json_data['behavior']['summary'].keys())
        except:
            pass
        
        
#     try:
#         n = len(json_data['signatures'])
#         for i in range(n):
#             try:
#                 p = len(json_data['signatures'][i]['marks'])
#                 for j in range(p):
#                     signature.add(json_data['signatures'][i]['marks'][j]['call']['api'])
#             except:
#                 pass
#     except:
#         pass
    
    f.close()

# print(signature)
print(summary)


