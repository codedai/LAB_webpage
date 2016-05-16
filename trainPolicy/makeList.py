import os

rootDir = './npy_final/'
# rootDir = "./data/"
for parent,dirnames,filenames in os.walk(rootDir):
    l =  len(filenames) // 2
    print (len(filenames))
    print (l)
    output = open('data.lst','w')
    # xx = 0
    for xx in range (l) :
        xxStr = '%d' % xx
        output.write(xxStr + '\t' + './npy_final/data_' + xxStr + '_.npy' + '\t' + './npy_final/label_' + xxStr + '_.npy' + '\n')
    output.close()
