import os
import os.path
import json
import shutil
from pprint import pprint as prt

'''
按照文件数量分文件夹
'''

# 文件按照固定数量分文件夹


def split_list_by_num(aim_list, Snum):
    to_list = zip(*(iter(aim_list),)*Snum)
    ed_list = [list(i) for i in to_list]
    count = len(aim_list) % Snum
    ed_list.append(aim_list[-count:]) if count != 0 else ed_list
    return ed_list

# 遍历并处置文件


def filesLists(root_dir, Snum):
    for root, dirs, files in os.walk(root_dir, False):
        prt(root)
        prt(dirs)

        # 是否是目标目录的判断
        if len(files) != 0 and len(files) > Snum:
            sp_res = split_list_by_num(files, Snum)

            # 目标文件夹处理
            file_list = {}
            for x in sp_res:
                t = sp_res.index(x)
                if t < 10:
                    root_p = root + '\\' + ' 00 ' + str(sp_res.index(x))
                if t < 100 and t >= 10:
                    root_p = root + '\\' + ' 0 ' + str(sp_res.index(x))
                if t < 1000 and t >= 100:
                    root_p = root + '\\' + str(sp_res.index(x))

                root_p = root_p.replace(' ', '')
                file_list[root_p] = x

                # 目录处理
                if not os.path.exists(root_p):
                    os.mkdir(root_p)

                # 移动文件
                for y in x:
                    old_path = root + '\\' + y
                    new_path = root_p + '\\' + y
                    print(old_path)
                    print(new_path)
                    shutil.move(old_path, new_path)

                # 生成目录列表
                json_path = root + '\\' + ' file_list.json '
                with open(json_path, 'w', encoding='utf-8') as f:
                    json.dump(file_list, f, ensure_ascii=False, indent=4)


def main():
    '''
    处理对应目录的文件
    '''
    root_dir = r'G:\down\123\mp4'

    # 每个文件夹的文件数量
    Snum = int(input('多少个文件放一个文件夹呢：'))
    # 文件处理
    filesLists(root_dir, Snum)


main()
