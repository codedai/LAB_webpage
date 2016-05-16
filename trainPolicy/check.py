import os
import checkPosition as sfg
import numpy as np
import os
import os.path
# import cPickle as pickle
# rootDir = "./data/"
rootDir = '/home/milab/workspace/Forxiuge/GO/'
targetDir = '../HA/'

for parent,dirnames,filenames in os.walk(rootDir):
    for filename in filenames:
        g = sfg.parse_file(rootDir + filename)
        print (filename)
        if g =='no':
            continue
        nodes = g.nodes
        while nodes.next is not None:
            error = nodes.node_str(True)
            if error == 'error position':
                os.system("rm " + rootDir + filename)
                break
            elif error == 'HA position':
                os.system("mv " + rootDir + filename + ' ' + targetDir)
            nodes = nodes.next
