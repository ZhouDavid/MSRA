import math
from matplotlib import pyplot as plt
import numpy as np
import os
import pandas as pd
import time
import cntk as C
import cntk.axis
from cntk.layers import Input,Dense,Dropout, Recurrence

def split_data(data,val_size=0.1,test_size=0.1):
	pos_test_index = int(len(data)*(1-test_size))
	pos_vali_index = int(pos_test_index*(1-val_size))
	train,test,vali = data[:pos_vali_index],data[pos_vali_index:pos_test_index],data[pos_test_index:]
	return {'train':train,'test':test,'val':vali}

def generate_data(fct,x,time_steps,time_shift):
	data = fct(x)
	#print(len(data))
	if not isinstance(data,pd.DataFrame):
		data = pd.DataFrame(dict(a = data[0:(len(data)-time_shift)],b=data[time_shift:]))
	rnn_x=[]
	for i in range(len(data)-time_steps):
		rnn_x.append(data['a'].iloc[i:i+time_steps])

	rnn_x = np.array(rnn_x)
	rnn_x = rnn_x.reshape(rnn_x.shape+(1,))
	rnn_y = data['b'].values
	rnn_y = rnn_y.reshape(rnn_y.shape+(1,))
	print(rnn_y.shape)

	return split_data(rnn_x),split_data(rnn_y)

N = 5
M = 5
X,Y=generate_data(np.sin,np.linspace(0,100,10000,dtype = np.float32),N,M)
f,a = plt.subplots(3,1,figsize=(12,8))
for j,ds in enumerate(['train','val','test']):
	a[j].plot(Y[ds],label=ds+'raw')
[i.legend() for i in a]

#plt.show()

def create_model(x):
	with C.layers.default_options(initial_state=0.1):
		m = C.layers.Recurrence(C.layers.LSTM(N))(x)
		m = C.ops.sequence.last(m)
		m = C.layers.Dropout(0.2)(m)
		m = C.layers.Dense(1)(m)
		return m
def next_batch(x,y,ds):
	def as_batch(data,start,count):
		part=[]
		for i in range(start,start+count):
			part.append(data[i])
		return np.array(part)
	for i in range(0,len(x[ds])-BATCH_SIZE,BATCH_SIZE):
		yield as_batch(x[ds],i,BATCH_SIZE),as_batch(y[ds],i,BATCH_SIZE)

TRAINING_STEPS = 10000
BATCH_SIZE=100
EPOCHS = 20

x = C.blocks.Input(1)
z = create_model(x)
l = C.blocks.Input(1,dynamic_axes = z.dynamic_axes,name='y')

learning_rate = 0.001
lr_schedule = C.learning_rate_schedule(learning_rate,C.UnitType.minibatch)

loss = C.ops.squared_error(z,l)
error = C.ops.squared_error(z,l)
momentum_time_constant = C.learner.momentum_as_time_constant_schedule(BATCH_SIZE / -math.log(0.9)) 
learner = C.learner.adam_sgd(z.parameters, lr = lr_schedule, momentum = momentum_time_constant, unit_gain = True)
trainer = C.Trainer(z, loss, error, [learner])

loss_summary=[]
start = time.time()
for epoch in range(0,EPOCHS):
	for x1,y1 in next_batch(X,Y,'train'):
		#print(x1,y1)
		trainer.train_minibatch({x:x1,l:y1})
	if epoch%(EPOCHS/10)==0:
		training_loss = C.utils.get_train_loss(trainer)
		loss_summary.append(training_loss)
		print("epoch:{},loss:{:.5f}".format(epoch,training_loss))
print("training took {0:.1f} seconds".format(time.time()-start))

plt.plot(loss_summary,label="training_loss")
def get_mse(X,Y,labeltxt):
    result = 0.0
    for x1, y1 in next_batch(X, Y, labeltxt):
        eval_error = trainer.test_minibatch({x : x1, l : y1})
        result += eval_error
    return result/len(X[labeltxt])

# Print the train and validation errors
for labeltxt in ["train", "val"]:
    print("mse for {}: {:.6f}".format(labeltxt, get_mse(X, Y, labeltxt)))
# Print validate and test error
labeltxt = "test"
print("mse for {}: {:.6f}".format(labeltxt, get_mse(X, Y, labeltxt)))
# predict
f, a = plt.subplots(3, 1, figsize = (12, 8))
for j, ds in enumerate(["train", "val", "test"]):
    results = []
    for x1, y1 in next_batch(X, Y, ds):
        pred = z.eval({x: x1})
        results.extend(pred[:, 0])
    a[j].plot(Y[ds], label = ds + ' raw');
    a[j].plot(results, label = ds + ' predicted');
[i.legend() for i in a];
plt.show()