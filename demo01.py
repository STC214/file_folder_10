import os
import re
import shutil
import os.path
from pprint import pprint as prt


def file_root_info(root_dir):
    for root, dirs, files in os.walk(root_dir):
        fi_list = []

        for i in files:
            if 'mp4' in i:
                fi_list.append(i)
        for i in files:
            if 'flv' in i:
                fi_list.append(i)
        for i in files:
            if 'mkv' in i:
                fi_list.append(i)

        if len(fi_list) != 0:
            # prt(root)
            eee = re.findall(pattern=(r'\d{3}\——\d{3}'), string=root)
            print(eee)
            sss = root
            if len(eee) > 1:
                ccc = root.split('\\')
                for i in range(1, len(eee)):
                    ccc.pop()
                sss = '\\'.join(ccc)
            prt(sss)


##########################################################################


file_root_info(r'H:\learn_video\Python数据分析课程')
