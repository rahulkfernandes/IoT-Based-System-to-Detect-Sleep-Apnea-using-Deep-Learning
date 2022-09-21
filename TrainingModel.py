# Accepts a ECG dataset and trains to classify them as apnea, no apnea.

import csv
import numpy as np
import pandas as pd
import os
import sys
import tensorflow as tf
from sklearn.model_selection import train_test_split


# Parameters
SAMPLE_SIZE= 2560000 #Number of samples
SAMPLE_FREQUENCY = 100
CLASSES = {
    'apnea':[1,0],
    #"borderline_apnea":[0,1,0],
    "no_apnea":[0,1]
}
EPOCHS=15
BATCH_SIZE=1
KERNEL_SIZE=4
FILTERS=64

def main():
    
    # handle improper usage.
    if len(sys.argv) != 2:
        sys.exit("Usage: apnea.py [dataset]")
        
    data_dir = sys.argv[1]
    print (f"ECG DATASET AT {data_dir}")

    # READING TRAINING DATASET
    train_data_dir = os.path.join(data_dir, "training_set")
    print("TRAINIGN DATASET IS LOADING FROM %s"%train_data_dir)
    traindataset, valdataset = load_train_data(train_data_dir)
    print("TRAIN DATASET SIZE")
    print(traindataset[0].shape, traindataset[1].shape)
    print(valdataset[0].shape, valdataset[1].shape)


    # CONVERTING NUMPY DATASET TO TENSORFLOW DATASET
    print("CONVERTING DATASET TO TENSORFLOW FORMAT") 
    traindataset = tf.data.Dataset.from_tensor_slices(traindataset)
    valdataset = tf.data.Dataset.from_tensor_slices(valdataset)

    traindataset = traindataset.batch(BATCH_SIZE)
    valdataset = valdataset.batch(BATCH_SIZE)

    print("CREATING MODEL USING KERAS")
    model = get_model()
    model.build((None, 2560000, 1))
    print(model.summary())
    model.compile(optimizer="adam",loss="categorical_crossentropy", metrics=["accuracy"]) 

    print("TRAINING MODEL")
    model.fit(traindataset, epochs=EPOCHS)

    print("evaluating model")
    model.evaluate(valdataset, verbose=2)
    # use test dataset with predict function
    
    #print("Predicting Model")
    #model.predict(testdataset, verbose=2)

    #TO SAVE THE MODEL
    model.save("./sleep_apnea_model.h5")

def load_train_data(data_dir):
    # data_dir = location of training dataset

    X = []
    y = []

    list_categories = os.listdir(data_dir)
    for cat in list_categories:
        list_files = os.listdir(os.path.join(data_dir, cat))

        for f in list_files:
            temp_data=pd.read_csv(os.path.join(data_dir, cat, f), index_col=0, header=0)
            print(f, temp_data.shape)

            temp = np.array([np.array([e])for e in temp_data['ECG']])

            X.append(temp)
            y.append(CLASSES[cat])
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2)

    return (np.array(X_train), np.array(y_train)), (np.array(X_val), np.array(y_val))


def get_model():

    model = tf.keras.models.Sequential([
        tf.keras.layers.Conv1D(filters=FILTERS, kernel_size=KERNEL_SIZE,activation="relu"),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.MaxPool1D(pool_size=(2)),
        tf.keras.layers.Dropout(0.5),

        tf.keras.layers.Conv1D(filters=FILTERS,kernel_size=KERNEL_SIZE, activation="relu"),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.MaxPool1D(pool_size=(2)),
        tf.keras.layers.Dropout(0.5),
        
        tf.keras.layers.Conv1D(filters=FILTERS,kernel_size=KERNEL_SIZE, activation="relu"),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.MaxPool1D(pool_size=(2)),
        tf.keras.layers.Dropout(0.5),

        tf.keras.layers.Conv1D(filters=FILTERS,kernel_size=KERNEL_SIZE, activation="relu"),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.MaxPool1D(pool_size=(2)),
        tf.keras.layers.Dropout(0.5),

        tf.keras.layers.Conv1D(filters=FILTERS,kernel_size=KERNEL_SIZE,activation="relu"),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.MaxPool1D(pool_size=(2)),
        tf.keras.layers.Dropout(0.5),

        tf.keras.layers.Conv1D(filters=FILTERS,kernel_size=KERNEL_SIZE,activation="relu"),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.MaxPool1D(pool_size=(2)),
        tf.keras.layers.Dropout(0.5),

        tf.keras.layers.Conv1D(filters=FILTERS,kernel_size=KERNEL_SIZE, activation="relu"),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.MaxPool1D(pool_size=(2)),
        tf.keras.layers.Dropout(0.5),

        tf.keras.layers.Conv1D(filters=FILTERS,kernel_size=KERNEL_SIZE, activation="relu"),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.MaxPool1D(pool_size=(2)),
        tf.keras.layers.Dropout(0.5),

        tf.keras.layers.Conv1D(filters=FILTERS,kernel_size=KERNEL_SIZE, activation="relu"),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.MaxPool1D(pool_size=(2)),
        tf.keras.layers.Dropout(0.5),

        tf.keras.layers.Conv1D(filters=FILTERS,kernel_size=KERNEL_SIZE,activation="relu"),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.MaxPool1D(pool_size=(2)), 
        tf.keras.layers.Dropout(0.5),

        tf.keras.layers.Flatten(),
        
        tf.keras.layers.Dense(512,activation="relu"),
        tf.keras.layers.Dropout(0.5),
        
        tf.keras.layers.Dense(512,activation="relu"),
        tf.keras.layers.Dropout(0.5),

        tf.keras.layers.Dense(512,activation="relu"),
        tf.keras.layers.Dropout(0.5),
    
        tf.keras.layers.Dense(512,activation="relu"),
        tf.keras.layers.Dropout(0.5),

        tf.keras.layers.Dense(2,activation="softmax")
    ])

    return model


#Filter & Normalization functions that were used for pre-processing
#def filter(ecg_signal):
    
#    #4th Order Butterworth Highpass Filter at 0.5Hz
#    highpass = 0.5
#    nyq = 0.5 * SAMPLE_FREQUENCY
#    cutoff = highpass / nyq
#    order = 4

#    b, a = scipy.signal.butter(order, cutoff, btype='highpass', analog=False)
#    y = scipy.signal.filtfilt(b, a, ecg_signal, axis=-1)
    
#    return (y)

#def normalise_signal(ecg_signal):
#    mean = ecg_signal.mean()
#    std = ecg_signal.std()
#    normalised_signal = []
#
#    for voltage in np.nditer(ecg_signal):
#        normalised_signal.append((
#            (voltage - mean) / std
#        ))
#    return np.array(normalised_signal)

if __name__ == "__main__":
    main()
