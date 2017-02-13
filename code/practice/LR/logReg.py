from __future__ import print_function
import numpy as np
import sys
import os
from cntk import Trainer, learning_rate_schedule, UnitType
from cntk.learner import sgd
from cntk.ops import *
import cntk
from cntk.utils import get_train_eval_criterion, get_train_loss
import matplotlib.pyplot as plt

cntk.device.set_default_device(cntk.device.cpu())

#generate data
input_dim = 2
num_output_classes = 2
mydict = {'w':None,'b':None}

def generate_random_data_sample(sample_size,feature_dim,num_classes):
	# Create synthetic data using NumPy. 
	Y = np.random.randint(size=(sample_size, 1), low=0, high=num_classes)

	# Make sure that the data is separable 
	X = (np.random.randn(sample_size, feature_dim)+3) * (Y+1)

	# Specify the data type to match the input variable used later in the tutorial 
	# (default type is double)
	X = X.astype(np.float32)    

	# converting class 0 into the vector "1 0 0", 
	# class 1 into vector "0 1 0", ...
	class_ind = [Y==class_number for class_number in range(num_classes)]
	Y = np.asarray(np.hstack(class_ind), dtype=np.float32)
    
	return X,Y

def linear_layer(input_var,output_dim):
	
	input_dim = input_var.shape[0]
	weight_param = parameter(shape=(input_dim,output_dim))
	bias_param = parameter(shape = (output_dim))
	mydict['w'],mydict['b'] = weight_param,bias_param
	#tmp = times(input_var,weight_param)+bias_param
	#print("middle output {},{}".format(tmp[0],tmp[1]))
	return times(input_var,weight_param)+bias_param
def moving_average(a,w=10):
	if len(a)<w:
		return a[:]
	return [val if idx<w else sum(a[(idx-w):idx])/w for idx,val in enumerate(a)]

def print_training_progress(trainer,mb,frequency,verbose = 1):
	training_loss,eval_error = "NA","NA"

	if mb % frequency == 0:
		training_loss = get_train_loss(trainer)
		eval_error = get_train_eval_criterion(trainer)
		if verbose: 
		    print ("Minibatch: {0}, Loss: {1:.4f}, Error: {2:.2f}".format(mb, training_loss, eval_error))
	return mb, training_loss, eval_error

if __name__ == '__main__':
	# sample_size = 32
	# features,labels = generate_random_data_sample(sample_size,input_dim,num_output_classes)
	# colors = ['r' if l==0 else 'b' for l in labels[:,0]]
	# plt.scatter(features[:,0],features[:,1],c=colors)
	# plt.xlabel('Scaled age')
	# plt.ylabel('Tumor size')
	
	input = input_variable(input_dim,np.float32)
	output_dim = num_output_classes
	z = linear_layer(input,output_dim)

	label = input_variable((num_output_classes),np.float32)
	loss = cross_entropy_with_softmax(z,label)
	eval_error = classification_error(z,label)

	learning_rate = 0.5
	lr_schedule= learning_rate_schedule(learning_rate,UnitType.minibatch)
	learner= sgd(z.parameters,lr_schedule)
	trainer = Trainer(z,loss,eval_error,[learner])

	minibatch_size = 25
	num_samples_to_train = 20000
	num_minibatches_to_train = int(num_samples_to_train / minibatch_size)

	training_progress_output_freq = 50
	plotdata = {"batchsize":[], "loss":[], "error":[]}

	for i in range(0, num_minibatches_to_train):
		features, labels = generate_random_data_sample(minibatch_size, input_dim, num_output_classes)

		# Specify input variables mapping in the model to actual minibatch data to be trained with
		trainer.train_minibatch({input : features, label : labels})
		batchsize, loss, error = print_training_progress(trainer, i, training_progress_output_freq, verbose=1)

		if not (loss == "NA" or error =="NA"):
		    plotdata["batchsize"].append(batchsize)
		    plotdata["loss"].append(loss)
		    plotdata["error"].append(error)