import os
import os.path
from pprint import pprint as pprt
import json
import shutil
import re

'''
整理目录中的教程文件
1.教程文件如果总体积大于500M则以不超过500M为标准分文文件夹保存
2.条件1中的最子级文件夹以此文件夹保存的教程视频序号区间命名
3.单个系列教程的根目录生成所有教程的文件列表文档
4.若文件名没有序号则添加序号
'''


# 文件名格式化处理
def strs_con(strs):
    constrs = strs.split('.')
    if len(constrs[0]) == 1:
        constrs[0] = '00' + constrs[0]
    elif len(constrs[0]) == 2:
        constrs[0] = '0' + constrs[0]
    else:
        pass
    strs = '.'.join(constrs)
    return strs


# 文件分文件夹归档方法
def file_move(dirs_dict):
    for k, v in dirs_dict.items():
        root_dirs, files_dict = k, v
        file_tmp_list = []
        size_count = 0

        # 文件名列表
        v_nl = []
        for x, y in files_dict.items():
            v_nl.append(x)

        for x, y in files_dict.items():
            size_count += files_dict[x]
            file_tmp_list.append(x)

            # 每次只处理500MB以下的数据内容
            if int(size_count / 1024 / 1024) > 500:
                # 列表和体积计数处理
                new_tmp_list = [file_tmp_list[-1], ]
                new_count = files_dict[file_tmp_list[-1]]
                file_tmp_list.pop()

                # 子文件夹命名处理
                for i in file_tmp_list:
                    constrs = i.split('.')
                    if file_tmp_list.index(i) == 0:
                        start_str = constrs[0]
                    if file_tmp_list.index(i) == len(file_tmp_list) - 1:
                        end_str = constrs[0]
                son_folder_name = root_dirs + '\\' + start_str + '——' + end_str
                # 判断文件夹是否存在
                if not os.path.exists(son_folder_name):
                    os.mkdir(son_folder_name)

                # 遍历文件并移动
                for i in file_tmp_list:
                    file_old_path = root_dirs + '\\' + i
                    file_new_path = son_folder_name + '\\' + i
                    shutil.move(file_old_path, file_new_path)

                file_tmp_list = new_tmp_list
                size_count = new_count

            if (int(size_count / 1024 / 1024) < 500) and (file_tmp_list[-1] == v_nl[-1]):
                # 子文件夹命名处理
                for i in file_tmp_list:
                    constrs = i.split('.')
                    if file_tmp_list.index(i) == 0:
                        start_str = constrs[0]
                    if file_tmp_list.index(i) == len(file_tmp_list) - 1:
                        end_str = constrs[0]
                son_folder_name = root_dirs + '\\' + start_str + '——' + end_str
                # 判断文件夹是否存在
                if not os.path.exists(son_folder_name):
                    os.mkdir(son_folder_name)

                # 遍历文件并移动
                pprt(file_tmp_list)
                for i in file_tmp_list:
                    file_old_path = root_dirs + '\\' + i
                    file_new_path = son_folder_name + '\\' + i
                    shutil.move(file_old_path, file_new_path)

        print('处理完成:' + root_dirs)


# 文件目录信息文档建立方法
def file_name(root_dirs):
    # 遍历目录中的所有目录和文件 root为当前文件所在目录 dir是当前目录下所有目录名组成的列表 files是所有文件名组成的列表
    for root, dirs, files in os.walk(root_dirs):

        if len(files) != 0:
            print(root)
            s = False
            for j in dirs:
                pattren = r'\d{3}\——\d{3}'
                if re.match(pattren, j):
                    s = True
                else:
                    s = False

            if s is False:
                for i in files:
                    file_pn = root + '\\' + i
                    file_npn = root + '\\' + strs_con(i)
                    # 文件重命名
                    os.rename(file_pn, file_npn)

                files = [strs_con(i) for i in files if ('file_list' not in i)]

                files.sort()
                pprt(files)

                dirs_dict = {}
                finfo_dict = {}

                # 文档目录拼接保存
                files_list_path = root + '\\file_list.txt'
                json_list_path = root + '\\file_list.json'

                with open(files_list_path, 'w', encoding='utf-8') as f:
                    list_strs = ''
                    for i in files:

                        if i != 'file_list.txt':
                            list_strs += (i + '\r')

                        file_size = os.path.getsize(root + '\\' + i)
                        print(file_size)

                        finfo_dict[i] = file_size
                        dirs_dict[root] = finfo_dict
                    f.write(list_strs)

                with open(json_list_path, 'w', encoding='utf-8') as f:

                    json.dump(dirs_dict, f, indent=4, ensure_ascii=False)
                pprt(dirs_dict)

                file_move(dirs_dict)


root_dirs = r'G:\down'
file_name(root_dirs)
