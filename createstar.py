# python2.7
# coding:utf-8
import os
import re

__author__ = 'WangYuchao'

import sys
import getopt

labels = ['_rlnMicrographName', '_rlnCoordinateX', '_rlnCoordinateY', '_rlnImageName',
          '_rlnDefocusU', '_rlnDefocusV', '_rlnDefocusAngle', '_rlnVoltage',
          '_rlnSphericalAberration', '_rlnAmplitudeContrast',
          '_rlnMagnification', '_rlnDetectorPixelSize', '_rlnCtfFigureOfMerit']

simplehead = """
data_

loop_
_rlnMicrographName #1
_rlnCoordinateX #2
_rlnCoordinateY #3
_rlnImageName #4
_rlnDefocusU #5
_rlnDefocusV #6
_rlnDefocusAngle #7
_rlnVoltage #8
_rlnSphericalAberration #9
_rlnAmplitudeContrast #10
_rlnMagnification #11
_rlnDetectorPixelSize #12
_rlnCtfFigureOfMerit #13
"""


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
        headdict.update({strlist[0][4:]: int(strlist[1].strip('#')) - 1})
    data = []
    for i in range(headlen - 1, len(lines)):
        if len(lines[i].split()) < 3:
            continue
        data.append(lines[i])
    f_star.close()
    return headdict, data


def getclassdata(filename, k):
    headdict, data = readstarfile(filename)
    newdata=[]
    for line in data:
        for classnum in k:
            if int(line.split()[headdict.get('ClassNumber', 0)]) == classnum:
                newdata.append(line)
    return headdict,newdata


def main():
    opts, args = getopt.getopt(sys.argv[1:], "dhi:o:s:k:")

    input_file = ""
    output_file = ""
    source_file = ""
    simp = 0
    k=[]

    if len(opts) == 0:
        usage()
        sys.exit()

    for op, value in opts:
        if op == "-i":
            input_file = value
        elif op == "-o":
            output_file = value
        elif op == "-s":
            source_file = value
        elif op == "-k":
            for i in value.split():
                k.append(int(i))
        elif op == "-d":
            simp = 1
        elif op == "-h":
            usage()
            sys.exit()

    if len(input_file) == 0:
        print("请添加输入文件 使用 -i file_name\n")
        sys.exit()

    if len(output_file) == 0:
        print("请添加输出文件名 使用 -o file_name\n")
        sys.exit()

    if len(source_file) == 0:
        print("请添加原文件 使用 -s file_name\n")
        sys.exit()

    if not os.path.exists(input_file):
        print("{} 文件不存在\n".format(input_file))
        sys.exit()

    if not os.path.exists(source_file):
        print("{} 文件不存在\n".format(source_file))
        sys.exit()

    if os.path.exists(output_file):
        print("{} 文件已经存在\n".format(output_file))
        sys.exit()

    if input_file.find('.star') != -1:
        if len(k) == 0:
            print "请输入需要提取的类的序号，使用 －k \"0,1\""
            sys.exit()
        headdict,data=getclassdata(input_file,k)


    f_input = open(input_file, 'r')  # 获取需要提取的序号
    str_index = f_input.readline()
    index = str_index.split()

    f_source = open(source_file, 'r')

    f_output = open(output_file, 'w')

    lines = f_source.readlines()

    head = 0
    for line in lines:
        if len(line.split()) < 3:
            head += 1
        else:
            break

    if simp == 1:
        labelindex = []
        for label in labels:  # 寻找需要的数据位置
            for i in range(head):
                if lines[i].find(label) != -1:
                    labelindex.append(int(re.findall("\d+", lines[i])[0]))
        # print(labelindex)
        # print(simplehead)
        f_output.write(simplehead)  # 写入精简后的文件头
        for i in index:
            item = lines[int(i) + head - 1].split()
            for j in labelindex:
                f_output.write("{}\t".format(item[j - 1]))
            f_output.write('\n')
    else:
        for i in range(head):
            f_output.write(lines[i])  # 写入标签头
        for i in index:
            f_output.write(lines[int(i) + head - 1])

    f_source.close()
    f_output.close()
    f_input.close()


def usage():
    print("""usage:
             -i:输入的序号文件名,请使用空格间隔
             -o:输出的star文件名
             -s:原始star文件名
             -h:帮助
    """)


if __name__ == '__main__':
    getclassdata('run_ct1_it002_data.star', 3)
