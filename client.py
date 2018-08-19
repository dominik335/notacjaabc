from __future__ import print_function

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
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.layers import GRU
from keras.optimizers import RMSprop
from keras.optimizers import Adam
from keras.callbacks import ModelCheckpoint
from keras.models import load_model
from sklearn.metrics import mean_squared_error
from keras.models import Sequential
from keras.layers import Dense
from methods import *

exec(sett)

def sample(seed):
    generated = ""
    for i in range(sample_len):
        # One hot encoding the input seed
        x = np.zeros((batch, seq_len, vocabulary))
        for seq_pos in range(seq_len):
            vocab_index = char_to_int[seed[seq_pos]]
            x[0, seq_pos, vocab_index] = 1
        # procuring the output (or prediction) from the network
        prediction = model.predict(x, batch_size=batch, verbose=0)
        prediction = prediction[0]

        # The prediction is an array of probabilities for each unique characters.
        prediction = np.asarray(prediction).astype('float64')
        prediction = np.log(prediction) / temperature  # Scaling prediction values with 'temperature'
        # to manipulate diversities.
        exp_preds = np.exp(prediction)
        prediction = exp_preds / np.sum(exp_preds)

        # Randomly an integer(mapped to a character) is chosen based on its likelihood
        # as described in prediction list

        RNG_int = np.random.choice(range(vocabulary), p=prediction.ravel())

        # The next character (to generate) is mapped to the randomly chosen integer
        # Procuring the next character from the dictionary by putting in the chosen integer
        next_char = int_to_char[RNG_int]
        generated = generated+next_char
        # Display the chosen character
        #sys.stdout.write(next_char)
        #sys.stdout.flush()
        # modifying seed for the next iteration for finding the next character
        seed = seed[1:] + next_char

    print()
    return (generated)

os.environ['TF_CPP_MIN_LOG_LEVEL']='3'

#misc

import os
from pandas import DataFrame
from pandas import concat
import tensorflow as tf

sample_len = 80

model_filename = "BestGRU.h5val.h5"
#model_filename = "BestGRU.h5"

modpath = "/home/dominik/Pulpit/MAGISTERKA/pobrane wagi/5/" + model_filename
model = load_model(modpath)
print ("Model loaded")

path = "/home/dominik/PycharmProjects/notacjaabc/cleaned"
inputf = "/home/dominik/Pulpit/MAGISTERKA/testoweMidiInput/1.abc"
outputf = inputf + "enriched.abc"

dataset = open(data_file).read()
dataset = convert(dataset)

chars = sorted(list(set(dataset)))
total_chars = len(dataset)
vocabulary = len(chars)
seed = open(inputf).read()
loadedcontent = seed

seed = convert(seed)
print("input len " + str(len(seed)))
seed = seed[-seq_len:]

print((vocabulary))
char_to_int = {c: i for i, c in enumerate(chars)}
int_to_char = {i: c for i, c in enumerate(chars)}
generated = ""
print((seed))

result = sample(seed)


print ("\n\n\ngenerated: "+ result)
print("\n\n"+ str(len(result)))

outfile = open(outputf, 'w')
outfile.write(loadedcontent+result)
outfile.close()