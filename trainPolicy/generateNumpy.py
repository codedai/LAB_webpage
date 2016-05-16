import sgfparser as sfg
import numpy as np
import os
import os.path
# import cPickle as pickle
# rootDir = "./data/"
rootDir = '/home/milab/workspace/Forxiuge/GO/'
# rootDir = "./data/"
for parent,dirnames,filenames in os.walk(rootDir):
    xx=0
    for filename in filenames:
        print (filename)
        g = sfg.parse_file(rootDir + filename)
        if g == 'no':
            continue
        nodes = g.nodes
        currrentPos = np.zeros((19,19))
        while nodes.next is not None:
            labelPos = np.zeros((19,19))
            # print xx
            nodes.node_str(True)
            if nodes.c == "B":
                # print ("B")
                # print (xx)
                if len(nodes.p) > 2:
                    currrentPos[nodes.dict[nodes.p[1]]][nodes.dict[nodes.p[2]]] = 1
                    # print currrentPos
                    xxStr = '%d' % xx
                    np.save('./npy_final/data_' + xxStr + '_.npy',currrentPos)
                    # print len(tatolChessBoard)
                    nodes = nodes.next
                    nodes.node_str(True)
                    # labelChess.append(nodes.chessboard)
                    if len(nodes.p) > 2:
                        labelPos[nodes.dict[nodes.p[1]]][nodes.dict[nodes.p[2]]] = 1
                    else:
                        labelPos[18][18] = 1
                    np.save('./npy_final/label_' + xxStr + '_.npy',labelPos)
                    xx += 1
                else:
                    nodes = nodes.next
                    # print currrentPos
            elif nodes.c == "W":
                # print ("W")
                # print (xx)
                if len(nodes.p) > 2:
                    currrentPos[nodes.dict[nodes.p[1]]][nodes.dict[nodes.p[2]]] = -1
                    xxStr = '%d' % xx
                    np.save('./npy_final/data_' + xxStr + '_.npy',currrentPos)
                    nodes = nodes.next
                    nodes.node_str(True)
                    # labelChess.append(nodes.chessboard)
                    if len(nodes.p) > 2:
                        labelPos[nodes.dict[nodes.p[1]]][nodes.dict[nodes.p[2]]] = 1
                    else:
                        labelPos[18][18] = 1
                    np.save('./npy_final/label_' + xxStr + '_.npy',labelPos)
                    xx += 1
                else:
                    nodes = nodes.next
                    # print currrentPos
            else:
                nodes = nodes.next

        print (filename)
#print len(All),len(All[1])
