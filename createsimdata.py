# python2.7
# coding:utf-8
import os


def genmrcs(clus, parnum=10000, snr=0.5):
    spi = open('genmrcs.spi', 'r')
    lines = spi.readlines()

    lines[3] = '[input] = \'{}\'\n'.format(clus)
    lines[4] = '[outputname] = \'{}_{}\'\n'.format(clus.split('.')[0], parnum)
    lines[6] = '[input_doc] = \'{}\'\n'.format(parnum)
    lines[13] = '[parnum] = \'{}\'\n'.format(parnum)
    lines[18] = '[SNR] = {}\n'.format(snr)

    spi.close()
    spi = open('genmrcs.spi', 'w')
    for line in lines:
        spi.write(line)
    spi.close()

    os.system('spider spi/dat @genmrcs')


cluses = []

files = os.listdir(os.getcwd() + '/Input')
print(files)

for f in files:
    print(f)
    print(os.path.isdir(f))
    if os.path.isfile('Input/{}'.format(f)):
        cluses.append(f.split('.')[0])

cluses.sort()
print(cluses)

for clus in cluses:
    genmrcs(clus)
