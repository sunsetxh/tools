import numpy as np
import sys



def readstarfile(filename):
    f_star = open(filename, 'r')
    lines = f_star.readlines()
    headlen = 0
    headdict = {}
    for line in lines:
        headlen += 1
        if len(line.split()) <= 1:
            continue
        elif len(line.split()) > 2:
            break
        strlist = line.split()
        # 将文件头信息存储到字典中
        headdict.update({strlist[0][4:]: int(strlist[1].strip('#')) - 1})
    data = []
    for i in range(headlen - 1, len(lines)):
        if len(lines[i].split()) < 3:
            continue
        data.append(lines[i])
    f_star.close()
    return headdict, data


file_diff2 = open(sys.argv[1], 'r')
i = -1
# group num 0 1 2 3 4
diff2 = []
temp = []

for line in file_diff2:
    items = line.split()
    if i == int(items[0]):
        temp.append(float(items[3]))
        continue
    elif i != -1:
        min_index = temp.index(min(temp[2:]))
        temp.append(min_index - 1)#添加最小值
        diff2_avg = float(np.average(temp[2:]))
        temp.append(diff2_avg)#添加均值
        # for j in temp[2:]):
        #   j -= diff2_min
        # temp.append(float(max(temp[2:]) - min(temp[2:])))
        # 添加差值
        if len(temp) == 6:
            temp.append(temp[2] - temp[3])
        else:
            temp.append(temp[temp[0] + 1] - temp[min_index])
        # 将该行数据添加至列表
        diff2.append(temp)
        if len(items) <= 1:
            break
        else:
            del temp
            temp = []

    if items[1].find('group') != -1:
        temp.append(int(items[1][items[1].index('group') + 5]))
        temp.append(int(items[1][0:(items[1].index('@'))]))
    else:
        temp.append(int(items[0]))
        if items[1].find('atp_0_160.mrcs') != -1:
            temp.append(0)
        else:
            temp.append(1)
    temp.append(float(items[3]))
    i = int(items[0])

diff2.sort()
output = open(sys.argv[2], 'w')
fmt = []
for item in diff2[0]:
    tpy = type(item)
    # print(item)
    # print(tpy)
    if tpy == int:
        fmt.append('{:6d}\t')
    elif tpy == float:
        fmt.append('{:8.2f}\t')
    elif tpy == str:
        fmt.append('{:6s}\t')
    else:
        fmt.append('{}\t')
# print(fmt)
for items in diff2:
    for i in range(len(items)):
        output.write(fmt[i].format(items[i]))
    output.write('\n')
output.close()
file_diff2.close()