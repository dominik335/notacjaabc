# Multilayered (or singlelayered) GRU based RNN for text generation using Keras libraries

# import libraries
from __future__ import print_function
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.layers import GRU
from keras.optimizers import RMSprop, Adam
from keras.callbacks import ModelCheckpoint
from keras.models import load_model
import numpy as np
import random
import sys
import os
import tensorflow as tf
from keras.callbacks import CSVLogger
from methods import *

exec(sett)
os.environ['TF_CPP_MIN_LOG_LEVEL']='1'


if gpu_restrict:
    config = tf.ConfigProto()
    config.gpu_options.per_process_gpu_memory_fraction = 0.8
    session = tf.Session(config=config)

dataset = open(data_file).read()
dataset = convert(dataset)

chars = sorted(list(set(dataset)))
total_chars = len(dataset)
vocabulary = len(chars)

print("Total Characters: ", total_chars)
print("Vocabulary: ", vocabulary)

# Creating dictionary or map in order to map all characters to an integer and vice versa
char_to_int = {c: i for i, c in enumerate(chars)}
int_to_char = {i: c for i, c in enumerate(chars)}

Answer = 0  # int(raw_input('Enter: '))


if Answer != 0:
    try:
        f = open('GRUModelInfo', "r")
        lines = f.readlines()
        for i in lines:
            thisline = i.split(" ")
        seq_len = int(thisline[0])
        batch = int(thisline[1])
        f.close()
    except:
        print("\nUh Oh! Caught some exceptions! May be you are missing the file having time step information")
        f = open('GRUModelInfo', 'w+')
        f.write(str(seq_len) + " " + str(batch))
        f.close()

if Answer == 0 or Answer == 2:


    index = int((total_chars - seq_len) / batch)
    index = batch * index
    dataset = dataset[:index + seq_len]

    total_chars = len(dataset)

    # prepare input data and output(target) data
    # (X signified Inputs and Y signifies Output(targeted-output in this case)
    dataX = []
    dataY = []

    for i in range(0, total_chars - seq_len):  # Example of an extract of dataset: Language
        dataX.append(dataset[i:i + seq_len])  # Example Input Data: Languag
        dataY.append(dataset[i + seq_len])  # Example of corresponding Target Output Data: e


    total_patterns = len(dataX)
    print("\nTotal Patterns: ", total_patterns)
    index = int((0.9*len(dataX)) / batch)
    print(index)
    index = index * batch
    print(index)
    trainPortion = int(index)

    # One Hot Encoding...
    X = np.zeros((total_patterns, seq_len, vocabulary), dtype=np.bool)
    Y = np.zeros((total_patterns, vocabulary), dtype=np.bool)

    for pattern in range(total_patterns):
        for seq_pos in range(seq_len):
            vocab_index = char_to_int[dataX[pattern][seq_pos]]
            X[pattern, seq_pos, vocab_index] = 1
        vocab_index = char_to_int[dataY[pattern]]
        Y[pattern, vocab_index] = 1


    Xtr = X[:trainPortion, :]
    Xval = X[trainPortion:, :]

    Ytr = Y[:trainPortion, :]
    Yval = Y[trainPortion:, :]


if use_previous_model == 0:
    # build the model: a multi(or single depending on user input)-layered GRU based RNN
    print('\nBuilding model...')

    model = Sequential()
    if hidden_layers == 1:
        model.add(GRU(neurons[0], batch_input_shape=(batch, seq_len, vocabulary), stateful=True))
    else:
        model.add(GRU(neurons[0], batch_input_shape=(batch, seq_len, vocabulary), stateful=True, return_sequences=True))
    model.add(Dropout(dropout_rate))
    for i in range(1, hidden_layers):
        if i == (hidden_layers - 1):
            model.add(GRU(neurons[i], stateful=True))
        else:
            model.add(GRU(neurons[i], stateful=True, return_sequences=True))
        model.add(Dropout(dropout_rate))

    model.add(Dense(vocabulary))
    model.add(Activation('softmax'))

    my_optimizer = RMSprop(lr=learning_rate)
    my_optimizer = Adam()
    model.compile(loss='categorical_crossentropy', optimizer=my_optimizer,metrics=['acc'])

    # save model information
    f = open('GRUModelInfo', 'w+')
    f.write(str(seq_len) + " " + str(batch))
    f.close()

else:
    print('\nLoading model...')
    try:
        model = load_model(model_filename)
        print("model loaded")
    except:
        print("\ncouldn't load model")
        sys.exit(0)
model.summary()

# define the checkpoint
checkpoint = ModelCheckpoint(model_filename, monitor='loss', verbose=1, save_best_only=True, mode='min')
checkpoint2 = ModelCheckpoint(model_filename+"val.h5", monitor='val_loss', verbose=1, save_best_only=True, mode='min')

csv_logger = CSVLogger('log.csv', append=True, separator=';')

# Function for creating a sample text from a random seed (an extract from the dataset).
# The seed acts as the input for the GRU RNN and after feed forwarding through the network it produces the output
# (the output can be considered to be the prediction for the next character)


if Answer == 0 or Answer == 2:
    # Train Model and print sample text at each epoch.

    for iteration in range(1, 60):
        print()
        print('Iteration: ', iteration)
        print()

        # Train model. If you have forgotten: X = input, Y = targeted outputs
        model.fit(Xtr, Ytr, batch_size=batch, epochs= epochs, validation_data=(Xval,Yval), shuffle=False, callbacks=[checkpoint,checkpoint2, csv_logger])
        model.save('mymodel.h5')  # Saving current model state so that even after terminating the program; training
        # can be resumed for last state in the next run.
        print()

        # Randomly choosing a sequence from dataset to serve as a seed for sampling
        start_index = random.randint(0, total_chars - seq_len - 1)
        seed = dataset[start_index: start_index + seq_len]
        print("sampling")
        sample(seed)
        print("sampled")

else:
    pass
