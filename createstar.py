# python2.7
# coding:utf-8
import os
import re

import operator

import time

__author__ = 'WangYuchao'

import sys
import getopt

labels = ['MicrographName', 'CoordinateX', 'CoordinateY', 'ImageName',
          'DefocusU', 'DefocusV', 'DefocusAngle', 'Voltage',
          'SphericalAberration', 'AmplitudeContrast',
          'Magnification', 'DetectorPixelSize', 'CtfFigureOfMerit']

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


# 将star文件读取到内存中
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


# 挑选出star文件中指定类的数据
def getclassdata(filename, k):
    headdict, data = readstarfile(filename)
    newdata = []
    for line in data:
        for classnum in k:
            if int(line.split()[headdict.get('ClassNumber', 0)]) == classnum:
                newdata.append(line)
    return headdict, newdata


# 存储star文件，支持原数据存储和简洁数据存储
def savestar(filename, headdict, data, simple=1):
    file = open(filename, 'w')
    if simple == 1:
        file.write(simplehead)
        labelitems = []
        for label in labels:
            labelitems.append(headdict.get(label, 0))
        for item in data:
            for j in labelitems:
                file.write('{}\t'.format(item.split()[j]))
            file.write('\n')
    else:
        file.write('\ndata_\n\nloop_\n')
        head = sorted(headdict.items(), key=operator.itemgetter(1))
        for name, value in head:
            file.write('_rln{} #{}\n'.format(name, value+1))
        for item in data:
            file.write(item)
    file.close()


def main():
    opts, args = getopt.getopt(sys.argv[1:], "dhi:o:s:k:")

    input_file = ""
    output_file = ""
    source_file = ""
    simp = 1
    k = []

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
            for i in value.split(','):
                k.append(int(i))
        elif op == "-d":
            simp = 0
        elif op == "-h":
            usage()
            sys.exit()

    if len(input_file) == 0:
        print("请添加输入文件 使用 -i file_name\n")
        sys.exit()

    # 如果没有指定输出文件名，自动命名
    if output_file == "":
        nowtime = time.strftime("%m%d%H%M%S")
        if source_file == "":
            output_file="class"
            for item in k:
                output_file+='-{}'.format(item)
            output_file+='-{}.star'.format(nowtime)
        else:
            output_file='{}.star'.format(input_file.split('.')[0])

    if len(source_file) == 0 and input_file.find('.star') == -1:
        print("请添加原文件 使用 -s file_name\n")
        sys.exit()

    if not os.path.exists(input_file):
        print("{} 文件不存在\n".format(input_file))
        sys.exit()

    if source_file != "" and not os.path.exists(source_file):
        print("{} 文件不存在\n".format(source_file))
        sys.exit()

    if os.path.exists(output_file):
        print("{} 文件已经存在\n".format(output_file))
        sys.exit()

    if input_file.find('.star') != -1:
        if len(k) == 0:
            print("请输入需要提取的类的序号，使用 －k 0,1")
            sys.exit()
        headdict, data = getclassdata(input_file, k)
        savestar(output_file, headdict, data, simp)
    else:
        f_input = open(input_file, 'r')  # 获取需要提取的序号
        str_index = f_input.readline()
        index = str_index.split()
        headdict, data = readstarfile(source_file)
        newdata = []
        for item in index:
            newdata.append(data[int(item)])
        savestar(output_file, headdict, newdata, simp)

        f_input.close()
        print('output file is {}'.format(output_file))


def usage():
    print("""usage:
             -i:输入的序号文件名,请使用空格间隔，如输入star文件，则需要参数k，不需要输入源文件
             -o:输出的star文件名
             -s:原始star文件名
             -k:需要匹配的类别，可以输入多个类，‘，’间隔
             -d:输出star文件中完整的信息
             -h:帮助
    """)


if __name__ == '__main__':
    main()
