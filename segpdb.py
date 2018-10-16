import sys

name = ''
if sys.argv[1]:
    name = sys.argv[1]
else:
    print('请输入原始文件')
    sys.exit()

source = open(name, 'r')

i = 0
outp = open('{}_{}.pdb'.format(name.split('.')[0], i),'w')
for line in source:
    if line.find('END') == -1:
        outp.write(line)
    else:
        outp.write('END')
        outp.close()
        i += 1
        outp = open('{}_{}.pdb'.format(name.split('.')[0], i),'w')

outp.close()
source.close()
