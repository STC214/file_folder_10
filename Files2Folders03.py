import os
import os.path
import json
import re
import shutil
from pprint import pprint as prt

'''
整理目录中的教程文件
1.教程文件如果总体积大于500M则以不超过500M为标准分文文件夹保存
2.条件1中的最子级文件夹以此文件夹保存的教程视频序号区间命名
3.单个系列教程的根目录生成所有教程的文件列表文档
4.若文件名没有序号则添加序号
5.除了视频主目录其他目录下没有列表文件
6.修复了mp4文件会被修改后缀的bug
'''


# 获取所有文件名并统一化改名
def get_filenames(root_dir):
    for root, dirs, files in os.walk(root_dir, False):

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
            print('\r\n')
            # prt(fi_list)

            for i in fi_list:
                tstr = i.replace('mp4', '')
                res = re.search(pattern=(r'\d{1,3}'), string=tstr)
                # prt(res.group(0))
                if res != None:
                    num_str = res.group(0)
                # print(len(num_str))
                q = i
                if len(num_str) == 1:
                    q = q.replace(num_str, ('00' + num_str), 1)
                if len(num_str) == 2:
                    q = q.replace(num_str, ('0' + num_str), 1)

                print(q)
                old_path = root + '\\' + i
                new_path = root + '\\' + q
                os.rename(old_path, new_path)


def save_file(root_dict, fi_list, json_path, txt_list_path):
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(root_dict, f, ensure_ascii=False, indent=4)

    with open(txt_list_path, 'w', encoding='utf-8') as f:
        strs = ''
        for p in fi_list:
            strs += p + '\r'
        f.write(strs)


# 目标子目录处理方法
def dir_con(dir_str):
    nalc = re.findall(pattern=(r'\d{3}\——\d{3}'), string=dir_str)
    if len(nalc) > 1:
        dirlist_old = dir_str.split('\\')
        pop_times = len(nalc)

        for i in range(1, pop_times):
            dirlist_old.pop()

        final_dir = '\\'.join(dirlist_old)
    else:
        final_dir = dir_str
    prt(final_dir)

    return final_dir


# 处理文件移动具体方法
def move_file(root_dict):
    try:
        file_tmp_list = []
        size_count = 0
        for k, v in root_dict.items():
            file_list = []
            for x, y in v.items():
                file_list.append(x)

            for x, y in v.items():
                file_tmp_list.append(x)
                size_count += y
                file_tmp_list.sort()
                if len(file_tmp_list) != 0:
                    # if len(file_tmp_list) > 1:
                    if int(size_count / 1024 / 1024) > 500:
                        # prt(file_tmp_list)
                        new_tmp_list = [file_tmp_list[-1], ]
                        new_count = v[file_tmp_list[-1]]

                        file_tmp_list.pop()

                        start_num = re.search(pattern=(r'\d{3}'), string=(file_tmp_list[0])).group(0)
                        print(start_num)
                        end_num = re.search(pattern=(r'\d{3}'), string=file_tmp_list[-1]).group(0)

                        son_dir_name = start_num + '——' + end_num
                        son_path = k + '\\' + son_dir_name
                        son_path = dir_con(son_path)

                        if not os.path.exists(son_path):
                            os.mkdir(son_path)

                        for i in file_tmp_list:
                            old_path = k + '\\' + i
                            new_path = son_path + '\\' + i
                            print(new_path)
                            # new_path = dir_con(new_path)
                            shutil.move(old_path, new_path)

                        file_tmp_list = new_tmp_list
                        size_count = new_count

                    if int(size_count / 1024 / 1024) < 500 and (file_list[-1] == file_tmp_list[-1]):
                        start_num = re.search(pattern=(r'\d{3}'), string=file_tmp_list[0]).group(0)
                        end_num = re.search(pattern=(r'\d{3}'), string=file_tmp_list[-1]).group(0)
                        son_dir_name = start_num + '——' + end_num
                        son_path = k + '\\' + son_dir_name
                        son_path = dir_con(son_path)

                        if not os.path.exists(son_path):
                            os.mkdir(son_path)

                        for i in file_tmp_list:
                            old_path = k + '\\' + i
                            new_path = son_path + '\\' + i
                            print(new_path)
                            # new_path = dir_con(new_path)
                            shutil.move(old_path, new_path)
                print('处理完成：' + k)
    except:
        pass


# 移动文件准备流程和调用移动文件方法
def file_move(root_dir):
    for root, dirs, files in os.walk(root_dir, False):
        # fi_list = files
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
            # print('\r\n')
            res_mol = False

            txt_list_path = root + '\\' + 'file_list.txt'
            json_path = root + '\\' + 'file_list.json'

            root_dict = {}
            dir_dict = {}

            for i in fi_list:
                file_path = root + '\\' + i
                # res_num = re.search(pattern=(r'\d{3}'), string=i).group(0)
                file_size = os.path.getsize(file_path)
                dir_dict[i] = file_size
            root_dict[root] = dir_dict

            if '——' not in json_path and "——" not in txt_list_path:
                save_file(root_dict, fi_list, json_path, txt_list_path)
            else:
                if os.path.exists(json_path):
                    os.remove(json_path)
                if os.path.exists(txt_list_path):
                    os.remove(txt_list_path)

            move_file(root_dict)


##################################################################################

def main():
    get_filenames(r'H:\learn_video')
    get_filenames(r'G:\down')
    get_filenames(r'E:\Program Files\JiJiDown\Download')
    file_move(r'H:\learn_video')
    # file_move(r'H:\learn_video\Python数据分析课程')
    file_move(r'G:\down')
    file_move(r'E:\Program Files\JiJiDown\Download')


main()
