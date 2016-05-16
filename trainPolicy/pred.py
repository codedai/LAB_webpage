import NpyIter as NI
from keras.models import Sequential
from keras.models import Graph
from keras.layers.core import Activation, Dense, Merge, Permute, Dropout
import numpy as np
# model = Sequential()
# model_a1 = Sequential()
# model_a2 = Sequential()
# model_a = Sequential()
# model_b1 = Sequential()
# model_b2 = Sequential()
# model_b = Sequential()
# model_c1 = Sequential()
# model_c2 = Sequential()
# model_c = Sequential()
# model_d1 = Sequential()
# model_d2 = Sequential()
# model_d = Sequential()
model = Graph()
from keras.layers.core import Dense, Activation

# model_a1.add(Dense(output_dim=1000, input_dim=361))
# model_a1.add(Activation("tanh"))
# model_a2.add(Dense(output_dim=1000, input_dim=361))
# model_a2.add(Activation("tanh"))
# model_a.add(Merge([model_a1, model_a2], mode='mul'))
# model_b2 = model_a
# model_a.add(Dense(output_dim=2000, input_dim=1000))
# model_b1 = model_a
# model_b1.add(Activation("tanh"))
# model_b2.add(Dense(output_dim=2000, input_dim=1000))
# model_b2.add(Activation("tanh"))
# model_b.add(Merge([model_b1, model_b2], mode='mul'))
# model_c2 = model_b
# model_b.add(Dense(output_dim=2000, input_dim=2000))
# model_c1 = model_b
# model_c1.add(Activation("tanh"))
# model_c2.add(Dense(output_dim=2000, input_dim=2000))
# model_c2.add(Activation("tanh"))
# model_c.add(Merge([model_c1, model_c2], mode='mul'))
# model_d2 = model_c
# model_c.add(Dense(output_dim=2000, input_dim=2000))
# model_d1 = model_c
# model_d1.add(Activation("tanh"))
# model_d2.add(Dense(output_dim=2000, input_dim=2000))
# model_d2.add(Activation("tanh"))
# model_d.add(Merge([model_d1, model_d2], mode='mul'))
# model = model_d
# model.add(Dense(output_dim=361))
# model.add(Activation("tanh"))
model.add_input(name='input',input_shape = (361,))
model.add_node(Dense(output_dim=361,input_dim=361),name='B1',input='input')
model.add_node(Activation('tanh'),name='B1_tanh',input='B1')
model.add_node(Dense(output_dim=361,input_dim=361),name='B2',input='input')
model.add_node(Activation('tanh'),name='B2_tanh',input='B2')
model.add_node(Dense(output_dim=361,input_dim=361),name='B', inputs=['B1_tanh', 'B2_tanh'], merge_mode='mul')
# model.add_node(Activation('tanh'),name='B_tanh',input='B')
model.add_node(Dense(output_dim=500,input_dim=361),name='C1_B',input='B')
model.add_node(Dense(output_dim=500,input_dim=361),name='C1_x',input='input')
model.add_node(Dense(output_dim=500,input_dim=500),name='C1', inputs=['C1_B', 'C1_x'], merge_mode='sum')
model.add_node(Activation('tanh'),name='C1_tanh',input='C1')
model.add_node(Dense(output_dim=500,input_dim=361),name='C2_B',input='B')
model.add_node(Dense(output_dim=500,input_dim=361),name='C2_x',input='input')
model.add_node(Dense(output_dim=500,input_dim=500),name='C2', inputs=['C2_B', 'C2_x'], merge_mode='sum')
model.add_node(Activation('tanh'),name='C2_tanh',input='C2')
model.add_node(Dense(output_dim=500,input_dim=500),name='C', inputs=['C1_tanh', 'C2_tanh'], merge_mode='mul')


model.add_node(Dense(output_dim=1000,input_dim=500),name='D1',input='C')
model.add_node(Activation('tanh'),name='D1_tanh',input='D1')
model.add_node(Dense(output_dim=1000,input_dim=500),name='D2',input='C')
model.add_node(Activation('tanh'),name='D2_tanh',input='D2')
model.add_node(Dense(output_dim=1000,input_dim=1000),name='D', inputs=['D1_tanh', 'D2_tanh'], merge_mode='mul')


model.add_node(Dense(output_dim=500,input_dim=1000),name='E1_B',input='D')
model.add_node(Dense(output_dim=500,input_dim=500),name='E1_x',input='C')
model.add_node(Dense(output_dim=500,input_dim=500),name='E1', inputs=['E1_B', 'E1_x'], merge_mode='sum')
model.add_node(Activation('tanh'),name='E1_tanh',input='E1')
model.add_node(Dense(output_dim=500,input_dim=1000),name='E2_B',input='D')
model.add_node(Dense(output_dim=500,input_dim=500),name='E2_x',input='C')
model.add_node(Dense(output_dim=500,input_dim=500),name='E2', inputs=['E2_B', 'E2_x'], merge_mode='sum')
model.add_node(Activation('tanh'),name='E2_tanh',input='E2')
model.add_node(Dense(output_dim=361,input_dim=500),name='E', inputs=['E1_tanh', 'E2_tanh'], merge_mode='mul')

model.add_output(name='output',input='E')
from keras.optimizers import SGD
# model.compile(optimizer=SGD(lr=0.01, momentum=0.9, nesterov=True),{'output':'mse'})
model.compile('rmsprop', {'output':'mse'})

# batch_size = 20000
# train_dataiter = NI.NpyIter(
# 	root_dir             = "./",
# 	flist_name           = "data.lst",
#     batch_size = batch_size
# 	)
# x = 0
# for data in train_dataiter:
#     # print data['data']
#     # import pdb; pdb.set_trace()
#     # print data['data']
#     # print data['softmax_label']
#     # print 'this is before the fit'
#     # print data
#     if  data is StopIteration:
#         break
#     else:
#         X_train = data['data']
#         Y_train = data['softmax_label']
#         print X_train.shape
#         model.fit({'input':X_train, 'output': Y_train}, nb_epoch=10, batch_size=10)
#
#     x+=1
#     if x % 50 == 0:
#         strx = '%d' % x
#         model.save_weights('model/fname_'+ strx +'.h5', overwrite=False)
#         test_dataiter = NI.NpyIter(
#         	root_dir             = "./",
#         	flist_name           = "demo.lst",
#             batch_size = 1244
#         	)
#         for test in test_dataiter:
#             if  test is StopIteration:
#                 break
#             else:
#                 X_test = data['data']
#                 Y_test = data['softmax_label']
#             predictions = model.predict({'input':X_test})
#             # print predictions.shape
#             np.save('./predict/predict_' + strx + '_.npy', predictions)
#
#     # print 'this is after fit'
# model. save_weights('model/fname_demo.h5', overwrite=False)
model.load_weights('model/fname_100.h5')
