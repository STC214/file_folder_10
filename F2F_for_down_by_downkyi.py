import os
import os.path
import json
import re
import shutil
import copy
import time
from pprint import pprint as prt


# 01.改文件名
def change_files_name(root_dir):
    for root, dirs, files in os.walk(root_dir, False):
        # prt(root)
        for i in files:
            fp = root + '\\' + i
            # print(fp)
            fn_control = i.split('.')
            # print(fn_control)

            # 多种文件名细节处理 for downkyi
            if ' ' in fn_control[0]:
                fn_control[0] = fn_control[0].replace(' ', '_')

            if '高清' in fn_control[0]:
                fn_control[0] = fn_control[0].replace('高清', '')

            if '1080P' in fn_control[0]:
                fn_control[0] = fn_control[0].replace('1080P', '')

            c_str = ['-', '(', ')', ',', '，', '。', ' ', '（', '）', '__', ' ']
            for q in c_str:
                fn_control[0] = fn_control[0].replace(q, '_')
                # 再来一次清楚双下划线
                for q in c_str:
                    fn_control[0] = fn_control[0].replace(q, '_')

            fnm01 = fn_control[0].split('_')
            fnum = fn_control[0].split('_')[0]
            if len(fnum) == 1:
                fnum = '000' + fnum

            elif len(fnum) == 2:
                fnum = '00' + fnum

            elif len(fnum) == 3:
                fnum = '0' + fnum

            # prt(fnum)+
            # prt(fn_control)
            nfn = fnum

            for i in range(1, (len(fnm01))):

                nfn = nfn + '_' + fnm01[i]

            nfn = nfn + '.mp4'

            nfp = root + '\\' + nfn

            # prt(nfp)

            # 文件改名
            os.rename(fp, nfp)


# 02 文件多次检查改名


def change_name(root_dir):
    for root, dirs, files in os.walk(root_dir, False):
        for i in files:
            if ' ' in i:
                prt('还有漏掉的，继续改吧')
                change_files_name(root_dir)

            else:
                prt('ok for name ' + i)


# 02.更改文件夹名
def change_folder_name(root_dir):
    for root, dirs, files in os.walk(root_dir):
        if len(files) != 0:
            # print(root)
            qp = root.split('\\')
            dn = qp[-1]

            c_str = ['-', '(', ')', ',', '，', '。',
                     ' ', '（', '）', '__', '+', '[', ']']
            res = False
            for i in c_str:
                if i in dn:
                    res = True

            patn = re.compile(r'\d{4}\——\d{4}')
            if patn.fullmatch(dn):
                print('分目录已经设置好了')
                # print(root)
            elif res == False:
                print('课程主目录已经设置好了')

            else:
                c_str = ['-', '(', ')', ',', '，', '。',
                         ' ', '（', '）', '__', '+']
                # print(root)
                for i in c_str:
                    dn = dn.replace(i, '_')

                # 再来一次消除双下划线
                for i in c_str:
                    dn = dn.replace(i, '_')

                dn = dn.replace('[', '【')
                dn = dn.replace(']', '】')

                print(dn)
                # 修改后的名字
                new_dp = root.replace(qp[-1], dn)
                print(new_dp)
                os.rename(root, new_dp)
                print('文件目录名称已修改')


# 03. 生成文件列表
def gen_file_list(root_dir):
    for root, dirs, files in os.walk(root_dir):

        prt(dirs)
        # time.sleep(1)

        if (len(files) == 2) and ('——' not in root) and ('filelist.json' in files):
            print('已经处理过了')

        # elif len(files) != 2 and '——' not in root:
        #     if ('filelist.json' in files) and('filelist.txt' in files):
        #         print('已经处理过了')
        #     else:
        #         print('???')

        else:
            prt(files)
            # 删掉已有的文件列表文件
            if 'filelist.json' in files:
                files.remove('filelist.json')
            if 'filelist.txt' in files:
                files.remove('filelist.txt')

            if (len(files) != 0) and ('——' not in root):
                # print(files)

                # prt(files)

                json_path = root + '\\' + 'filelist.json'
                txt_path = root + '\\' + 'filelist.txt'
                with open(json_path, 'w', encoding='utf-8') as f:
                    json.dump(files, f, ensure_ascii=False, indent=4)

                with open(txt_path, 'w', encoding='utf-8') as f:
                    strs = ''
                    for p in files:
                        strs += p + '\r'
                    f.write(strs)

# 04.移动文件
def move_file(root_dir):
    for root, dirs, files in os.walk(root_dir):
        if len(files) > 2 and '——' not in root:
            fdetail = {}
            files.pop(-1)
            files.pop(-1)
            for i in files:
                fp = root + '\\' + i
                fsz = os.path.getsize(fp)
                fdetail[i] = fsz
            prt(fdetail)

            count_o500 = 0
            size_count = 0
            for k, v in fdetail.items():
                # print(v)

                if (int(v) / 1024 / 1024) > 500:
                    count_o500 += 1
                # print(count_o500)
                size_count += v
                # print(size_count)

            if (count_o500 / len(fdetail)) >= 0.5:
                print('当前文件夹文件过大，不处理')

            else:
                 # 判断教程文件目录中的所有文件的大小
                # 超过500M的处理方式
                if int(size_count / 1024 / 1024) > 500:
                    size_count_0 = 0
                    file_list = []
                    file_num_list = []
                    for k, v in fdetail.items():
                        # print(k)
                        # print(v)
                        file_list.append([k, v])

                    # prt(file_list)
                    ed_fl = copy.copy(file_list)

                    for fl in file_list:
                        if isinstance(fl[1], int):
                            size_count_0 += fl[1]
                            file_num_list.append(fl[0])
                            if int(fl[1] / 1024/1024) > 500:
                                pass
                            elif int(size_count_0 / 1024 / 1024) > 500 and isinstance(fl[-1], int) and int(fl[1] / 1024/1024) < 500:
                                # prt(file_list)

                                start_num = (file_num_list[0].split('_'))[0]

                                final_li = copy.copy(file_num_list)
                                if len(file_num_list) > 1:
                                    if file_num_list[-1] != file_list[-1][0]:
                                        end_mum = (
                                            file_num_list[-2].split('_'))[0]
                                        final_li.pop(-1)
                                    else:
                                        end_mum = (
                                            file_num_list[-1].split('_'))[0]
                                else:
                                    end_mum = start_num

                                new_path_name = start_num + '——' + end_mum

                                print('='*79 + '\n')
                                print('新目录的名:%s' % new_path_name)

                                if not os.path.exists(root + '\\' + new_path_name):
                                    os.makedirs(root + '\\' + new_path_name)

                                for fi in final_li:
                                    old_path = root + '\\' + fi
                                    new_path = root + '\\' + new_path_name + '\\' + fi
                                    print('未整理的目录是%s' % old_path)
                                    print('已整理的目录是%s' % new_path)
                                    shutil.move(old_path, new_path)

                                prt(final_li)

                                file_num_list = [file_num_list[-1]]

                                size_count_0 = fl[1]
                            elif int(size_count_0 / 1024 / 1024) < 500 and (file_num_list[-1] == file_list[-1][0]):
                                start_num = (file_num_list[0].split('_'))[0]
                                end_mum = (file_num_list[-1].split('_'))[0]
                                new_path_name = start_num + '——' + end_mum

                                if not os.path.exists(root + '\\' + new_path_name):
                                    os.makedirs(root + '\\' + new_path_name)

                                for fi in file_num_list:
                                    old_path = root + '\\' + fi
                                    new_path = root + '\\' + new_path_name + '\\' + fi
                                    print('未整理的目录是%s' % old_path)
                                    print('已整理的目录是%s' % new_path)
                                    shutil.move(old_path, new_path)
                            else:
                                print('已经完成了或者出现了意料之外的情况')

                # 不到500M的处理方式
                if int(size_count / 1024 / 1024) < 500:
                    file_num_list = []
                    for k, v in fdetail.items():
                        str_num = (k.split('_'))[0]
                        file_num_list.append(str_num)
                    # prt(file_num_list)
                    folder_name = file_num_list[0] + '——' + file_num_list[-1]
                    # prt(folder_name)
                    # prt(root)
                    file_new_path = root + '\\' + folder_name
                    prt(file_new_path)
                    for file in files:
                        old_path = root + '\\' + file
                        new_path = file_new_path + '\\' + file
                        prt(old_path)
                        prt(new_path)
                        if not os.path.exists(file_new_path):
                            os.makedirs(file_new_path)

                        shutil.move(old_path, new_path)
                        print('移动成功了')


def main():
    # root_dir = r'K:\教程\安卓逆向\【Golang】_20天入门到精通Go语言_最新培训班带学生推荐_'
    # root_dir = r'K:\教程\202005'
    root_dir = r'F:\learn_video'

    change_name(root_dir)
    change_folder_name(root_dir)
    gen_file_list(root_dir)
    move_file(root_dir)


main()
