# python2.7
# coding:utf-8
import os
import operator
import threading
import time

# 存储star文件，支持原数据存储和简洁数据存储
import sys


def savestar(filename, headdict, data):
    file = open(filename, 'w')
    file.write('\ndata_\n\nloop_\n')
    head = sorted(headdict.items(), key=operator.itemgetter(1))
    for name, value in head:
        file.write('_rln{0} #{1}\n'.format(name, value + 1))
    for item in data:
        file.write(item)
    file.close()


def genmrcs(clusname, outputdir, parnum, snr):
    os.system('mkdir -p {0}/{1}'.format(outputdir, clusname))

    angledocs = '{0}/{1}/angledocs'.format(outputdir, clusname)
    shiftdocs = '{0}/{1}/shiftdocs'.format(outputdir, clusname)
    ctfdocs = '{0}/{1}/ctfdocs'.format(outputdir, clusname)

    spi = open('genmrcs.spi', 'r')
    lines = spi.readlines()

    lines[3] = '[input] = \'Input/{0}\'\n'.format(clusname)
    lines[4] = '[outputname] = \'{0}/{1}/{2}\'\n'.format(outputdir, clusname, clusname)
    lines[6] = '[input_doc] = \'{0}\'\n'.format(parnum)
    lines[7] = '[angledocs] = \'{0}\'\n'.format(angledocs)
    lines[8] = '[shiftdocs] = \'{0}\'\n'.format(shiftdocs)
    lines[9] = '[ctfdocs]   = \'{0}\'\n'.format(ctfdocs)
    lines[10] = '[relionoutput] = \'{0}/Image/{1}\'\n'.format(outputdir, clusname)
    lines[13] = '[parnum] = {0}\n'.format(parnum)
    lines[18] = '[SNR] = {0}\n'.format(snr)
    lines[
        155] = 'relion_preprocess --operate_on [outputname].dat --operate_out [relionoutput] --norm --bg_radius {***[radius]}\n'

    spi.close()
    spi = open('genmrcs.spi', 'w')
    for l in lines:
        spi.write(l)
    spi.close()

    os.system('spider spi/dat @genmrcs')
    print('{0} finished'.format(clusname))


os.system('mkdir Output')

cluses = []
files = os.listdir(os.getcwd() + '/Input')

for f in files:
    if os.path.isfile('Input/{0}'.format(f)):
        cluses.append(f.split('.')[0])

cluses.sort()
print(cluses)
if len(sys.argv) > 1:
    snr = float(sys.argv[1])
else:
    snr = 0.1
parnum = 10000
opdirs = []
outputdir = 'Output/snr{0}'.format(int(snr * 10))
os.system('mkdir -p {0}/Image'.format(outputdir))
threads = []
for clus in cluses:
    clusname = clus.split('.')[0]
    opdirs.append('{0}/{1}'.format(outputdir, clusname))
    t = threading.Thread(target=genmrcs, args=(clusname, outputdir, parnum, snr,))
    threads.append(t)
for t in threads:
    t.start()
    time.sleep(30)
for t in threads:
    t.join()

print('start to create star file')
headdict = {'Voltage': 0, 'DefocusU': 1, 'DefocusV': 2, 'DefocusAngle': 3, 'SphericalAberration': 4,
            'AmplitudeContrast': 5,
            'ImageName': 6}
data = []
for dir in opdirs:
    anglefile = open('{0}/angledocs.dat'.format(dir), 'r')
    shiftfile = open('{0}/shiftdocs.dat'.format(dir), 'r')
    ctffile = open('{0}/ctfdocs.dat'.format(dir), 'r')
    anglelines = anglefile.readlines()
    shiftlines = shiftfile.readlines()
    ctflines = ctffile.readlines()
    for i in range(1, parnum + 1):
        angleitems = anglelines[i].split()
        shiftitems = shiftlines[i].split()
        ctfitems = ctflines[i].split()
        line = '{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6:6d}@{7}/{8}.mrcs\n'.format(
            ctfitems[0],
            ctfitems[2],
            ctfitems[3],
            ctfitems[4],
            ctfitems[5],
            ctfitems[6],
            i,
            'Image', dir.split('/')[2])
        data.append(line)

savestar('Output/snr{0}/total.star'.format(int(snr * 10)), headdict, data)
