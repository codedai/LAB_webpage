import NPYI as NI
from keras.models import Sequential
from keras.models import Graph
from keras.layers.core import Activation, Dense, Merge, Permute, Dropout
import numpy as np

model = Graph()
from keras.layers.core import Dense, Activation

all=np.load('weight_demo/weight_30_final.npy')

model.add_input(name='input',input_shape = (361,))
model.add_node(Dense(output_dim=400,input_dim=361),name='B1',input='input')
model.add_node(Activation('tanh'),name='B1_tanh',input='B1')
model.add_node(Dense(output_dim=400,input_dim=361),name='B2',input='input')
model.add_node(Activation('relu'),name='B2_tanh',input='B2')
model.add_node(Dense(output_dim=400,input_dim=400),name='B', inputs=['B1_tanh', 'B2_tanh'], merge_mode='mul')
# model.add_node(Activation('tanh'),name='B_tanh',input='B')
model.add_node(Dense(output_dim=600,input_dim=400),name='C1_B',input='B')
model.add_node(Dense(output_dim=600,input_dim=361),name='C1_x',input='input')
model.add_node(Dense(output_dim=600,input_dim=600),name='C1', inputs=['C1_B', 'C1_x'], merge_mode='sum')
model.add_node(Activation('tanh'),name='C1_tanh',input='C1')
model.add_node(Dense(output_dim=600,input_dim=400),name='C2_B',input='B')
model.add_node(Dense(output_dim=600,input_dim=361),name='C2_x',input='input')
model.add_node(Dense(output_dim=600,input_dim=600),name='C2', inputs=['C2_B', 'C2_x'], merge_mode='sum')
model.add_node(Activation('relu'),name='C2_tanh',input='C2')
model.add_node(Dense(output_dim=600,input_dim=600),name='C', inputs=['C1_tanh', 'C2_tanh'], merge_mode='mul')


model.add_node(Dense(output_dim=800,input_dim=600),name='D1',input='C')
model.add_node(Activation('tanh'),name='D1_tanh',input='D1')
model.add_node(Dense(output_dim=800,input_dim=600),name='D2',input='C')
model.add_node(Activation('relu'),name='D2_tanh',input='D2')
model.add_node(Dense(output_dim=800,input_dim=800),name='D', inputs=['D1_tanh', 'D2_tanh'], merge_mode='mul')


model.add_node(Dense(output_dim=1000,input_dim=800),name='E1_B',input='D')
model.add_node(Dense(output_dim=1000,input_dim=600),name='E1_x',input='C')
model.add_node(Dense(output_dim=1000,input_dim=1000),name='E1', inputs=['E1_B', 'E1_x'], merge_mode='sum')
model.add_node(Activation('tanh'),name='E1_tanh',input='E1')
model.add_node(Dense(output_dim=1000,input_dim=800),name='E2_B',input='D')
model.add_node(Dense(output_dim=1000,input_dim=600),name='E2_x',input='C')
model.add_node(Dense(output_dim=1000,input_dim=1000),name='E2', inputs=['E2_B', 'E2_x'], merge_mode='sum')
model.add_node(Activation('relu'),name='E2_tanh',input='E2')
model.add_node(Dense(output_dim=1000,input_dim=1000),name='E', inputs=['E1_tanh', 'E2_tanh'], merge_mode='mul')

model.add_node(Dense(output_dim=361,input_dim=1000),name='F',input='E')
model.add_node(Activation('softmax'),name='F_soft',input='F')

model.add_output(name='output',input='F_soft')
# from keras.optimizers import SGD
# sgd = SGD(lr=0.0005, nesterov=True)
from keras.optimizers import Adam
adam = Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=1e-08)
model.compile(adam,{'output':'categorical_crossentropy'})
#model.compile('rmsprop', {'output':'mse'})
j = 0
print ('Initializing the weights...')
for i in range(0,len(model.layers)):
	if model.layers[i].get_weights()!=[]:
		if j > 40:
			print ('OOPS......ERROR')
			break
		model.layers[i].set_weights([all[j],all[j+1]])
		j = j + 2

for epoch in range(31,50):
	batch_size = 2000000
	train_dataiter = NI.NpyIter(
		root_dir             = "./",
		flist_name           = "data.lst",
	    batch_size = batch_size
		)
	x = 0
	i = 0
	for data in train_dataiter:
		if data is StopIteration:
			break
		else:
			i+=1
			X_train = data['data']
			Y_train = data['softmax_label']
			model.fit({'input':X_train, 'output':Y_train}, nb_epoch=1, batch_size=16)
		print ("This is in epoch %d's %dth iteration", epoch, x)

	if epoch % 1 == 0:
		strx = '%d' % epoch
		model.save_weights('weight/NN_' + strx + '.h5', overwrite=True)
		model_weight = model.get_weights()
		np.save('weight/weight_' + strx + '_final', model_weight)

		test_dataiter = NI.NpyIter(
			root_dir = "./",
			flist_name = 'test.lst',
			batch_size = 1
		)

		count = 0
		for test in test_dataiter:
			if test is StopIteration:
				break
			else:
				X_test = test['data']
				Y_test = test['softmax_label']
				predictions = model.predict({'input':X_test})
				b = predictions.get('output')
				_positon = np.argmax(abs(b))
				l_positon = np.argmax(abs(Y_test))
				if _positon == l_positon:
					count += 1
		print(count)
		np.save('./predict/predict_label_'+ strx + '-.npy', Y_test)
		np.save('./predict/predict_output_'+ strx + '-.npy', predictions)
		np.save('./predict/predict_'+ strx + '-.npy', Y_test)
model.save_weights('model/NN_final.h5', overwrite=True)
model.load_weights('model/NN_final.h5')
