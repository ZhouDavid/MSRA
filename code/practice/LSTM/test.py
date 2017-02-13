import math
from matplotlib import pyplot as plt
import numpy as np
import os
import pandas as pd
import time

import cntk as C
import cntk.axis
from cntk.layers import Input, Dense, Dropout, Recurrence 
if 'TEST_DEVICE' in os.environ:
    import cntk
    if os.environ['TEST_DEVICE'] == 'cpu':
        C.device.set_default_device(C.device.cpu())
    else:
        C.device.set_default_device(C.device.gpu(0))
isFast = True
def split_data(data, val_size=0.1, test_size=0.1):
    """
    splits np.array into training, validation and test
    """
    pos_test = int(len(data) * (1 - test_size))
    pos_val = int(len(data[:pos_test]) * (1 - val_size))

    train, val, test = data[:pos_val], data[pos_val:pos_test], data[pos_test:]

    return {"train": train, "val": val, "test": test}

def generate_data(fct, x, time_steps, time_shift):
    """
    generate sequences to feed to rnn for fct(x)
    """
    data = fct(x)
    if not isinstance(data, pd.DataFrame):
        data = pd.DataFrame(dict(a = data[0:len(data) - time_shift],
                                 b = data[time_shift:]))
    rnn_x = []
    for i in range(len(data) - time_steps):
        rnn_x.append(data['a'].iloc[i: i + time_steps].as_matrix())
    rnn_x = np.array(rnn_x)

    # Reshape or rearrange the data from row to columns
    # to be compatible with the input needed by the LSTM model
    # which expects 1 float per time point in a given batch
    rnn_x = rnn_x.reshape(rnn_x.shape + (1,))
    
    rnn_y = data['b'].values
    
    # Reshape or rearrange the data from row to columns
    # to match the input shape
    rnn_y = rnn_y.reshape(rnn_y.shape + (1,))

    return split_data(rnn_x), split_data(rnn_y)

N = 5 # input: N subsequent values 
M = 5 # output: predict 1 value M steps ahead
X, Y = generate_data(np.sin, np.linspace(0, 100, 10000, dtype=np.float32), N, M)

f, a = plt.subplots(3, 1, figsize=(12, 8))
for j, ds in enumerate(["train", "val", "test"]):
    a[j].plot(Y[ds], label=ds + ' raw');
[i.legend() for i in a];


def create_model(x):
    """Create the model for time series prediction"""
    with C.layers.default_options(initial_state = 0.1):
        m = C.layers.Recurrence(C.layers.LSTM(N))(x)
        m = C.ops.sequence.last(m)
        m = C.layers.Dropout(0.2)(m)
        m = cntk.layers.Dense(1)(m)
        return m
def next_batch(x, y, ds):
    """get the next batch to process"""

    def as_batch(data, start, count):
        part = []
        for i in range(start, start + count):
            part.append(data[i])
        return np.array(part)

    for i in range(0, len(x[ds])-BATCH_SIZE, BATCH_SIZE):
        yield as_batch(x[ds], i, BATCH_SIZE), as_batch(y[ds], i, BATCH_SIZE)

TRAINING_STEPS = 10000
BATCH_SIZE = 100
EPOCHS = 20 if isFast else 100

# input sequences
x = C.blocks.Input(1)

# create the model
z = create_model(x)

# expected output (label), also the dynamic axes of the model output
# is specified as the model of the label input
l = C.blocks.Input(1, dynamic_axes=z.dynamic_axes, name="y")

# the learning rate
learning_rate = 0.001
lr_schedule = C.learning_rate_schedule(learning_rate, C.UnitType.minibatch)

# loss function
loss = C.ops.squared_error(z, l)

# use squared error to determine error for now
error = C.ops.squared_error(z, l)

# use adam optimizer
momentum_time_constant = C.learner.momentum_as_time_constant_schedule(BATCH_SIZE / -math.log(0.9)) 
learner = C.learner.adam_sgd(z.parameters, 
                             lr = lr_schedule, 
                             momentum = momentum_time_constant, 
                             unit_gain = True)
trainer = C.Trainer(z, loss, error, [learner])

# train
loss_summary = []
start = time.time()
for epoch in range(0, EPOCHS):
    for x1, y1 in next_batch(X, Y, "train"):
        trainer.train_minibatch({x: x1, l: y1})
    if epoch % (EPOCHS / 10) == 0:
        training_loss = cntk.utils.get_train_loss(trainer)
        loss_summary.append(training_loss)
        print("epoch: {}, loss: {:.5f}".format(epoch, training_loss))

print("training took {0:.1f} sec".format(time.time() - start))