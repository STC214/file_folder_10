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
7.修复了以前会创建多层目录保存file_list文件的bug
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
                if res is not None:
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


# 处理记录列表的bug
def path_con_for_list(f_path):
    path_splited = f_path.split('\\')
    files_name = path_splited.pop()
    path_splited.pop()
    # print(path_splited)
    root_path = '\\'.join(path_splited)

    return files_name, path_splited, root_path


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

                        start_num = re.search(
                            pattern=(r'\d{3}'), string=(file_tmp_list[0])).group(0)
                        print(start_num)
                        end_num = re.search(
                            pattern=(r'\d{3}'), string=file_tmp_list[-1]).group(0)

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
                        start_num = re.search(
                            pattern=(r'\d{3}'), string=file_tmp_list[0]).group(0)
                        end_num = re.search(
                            pattern=(r'\d{3}'), string=file_tmp_list[-1]).group(0)
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
    except Exception as e:
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
            # res_mol = False

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


def gen_txt_json(root_dir):
    fil_list = []
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
            for i in fi_list:
                ffp = root + '\\' + i
                fil_list.append(ffp)

    nef = sorted(fil_list)

    fl = []
    fd = {}
    for f in range(1, len(nef)):
        files_name, path_splited, root_path = path_con_for_list(nef[f])
        fn_1, ps_1, rp_1 = path_con_for_list(nef[f - 1])
        txt_path = rp_1 + '\\' + 'file_list.txt'
        json_path = rp_1 + '\\' + 'file_list.json'

        if path_splited == ps_1:
            fl.append(fn_1)
            fl.append(files_name)
            fl = sorted(list(set(fl)))
            fd[rp_1] = fl

        if path_splited != ps_1 and (fl != []) and (fd != {}):
            save_file(fd, fl, json_path, txt_path)
            fl = []
            fd = {}

        if f == len(nef) - 1:
            save_file(fd, fl, json_path, txt_path)

        prt(fl)
        prt(fd)


def del_more_log(root_dir):
    for root, dirs, files in os.walk(root_dir, False):
        for i in files:
            if ('file_list.txt' in i) or ('file_list.json' in i):
                if root.count('——') >= 2:
                    print(root)
                    if os.path.exists(root):
                        shutil.rmtree(root)


##################################################################################

def main():
    path_list = [r'H:\learn_video', r'G:\down',
                 r'E:\Program Files\JiJiDown\Download']
    # path_list = [r'E:\Program Files\JiJiDown\Download']
    # pathi = r'E:\Program Files\JiJiDown\Download'
    for pathi in path_list:
        get_filenames(pathi)
        file_move(pathi)
        gen_txt_json(pathi)
        del_more_log(pathi)


main()
