import numpy as np

from keras.models import Sequential
from keras.layers import Activation, Dense
from keras.layers import LSTM
import keras


# TODO: fill out the function below that transforms the input series 
# and window-size into a set of input/output pairs for use with our RNN model
def window_transform_series(series, window_size):
    # containers for input/output pairs
    dtype = type(series[0])
    X = np.zeros((len(series)-window_size, window_size), dtype=dtype)
    y = np.zeros((len(series)-window_size, 1), dtype=dtype)

    i = 0
    for p in range(window_size, len(series)):
        X[i] = series[p-window_size:p]
        y[i] = series[p]
        i += 1
    
    return X,y

# TODO: build an RNN to perform regression on our time series input/output data
def build_part1_RNN(window_size):
    model = Sequential()
    model.add(LSTM(5, input_shape=(window_size, 1)))
    model.add(Dense(1))
    return model


### TODO: return the text input with only ascii lowercase and the punctuation given below included.
def cleaned_text(text):
    punctuation = ['!', ',', '.', ':', ';', '?']
    chars = set(text)
    charcount = []
    for char in chars:
        charcount.append([char, text.count(char)])
    charcount.sort(key=lambda x: x[1])
    i = 0
    while charcount[i][0] != 'z':
        print(charcount[i][0])
        if charcount[i][0] not in punctuation:
            text = text.replace(charcount[i][0], ' ')
        i += 1
        print(charcount[i][0] in text)
    return text

### TODO: fill out the function below that transforms the input text and window-size into a set of input/output pairs for use with our RNN model
def window_transform_text(text, window_size, step_size):
    # containers for input/output pairs
    inputs = []
    outputs = []
    
    i = 0
    for p in range(window_size, len(text), step_size):
        inputs.append(text[p-window_size:p])
        outputs.append(text[p])
        i += 1
    return inputs,outputs

# TODO build the required RNN model: 
# a single LSTM hidden layer with softmax activation, categorical_crossentropy loss 
def build_part2_RNN(window_size, num_chars):
    model = Sequential()
    model.add(LSTM(200, input_shape=(window_size, num_chars)))
    model.add(Dense(num_chars))
    model.add(Activation('softmax'))
    return model
