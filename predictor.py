import pandas as pd
from scipy.signal import filtfilt
import scipy
import numpy as np
import tensorflow as tf
from const import SAMPLE_FREQUENCY, CATEGORIES, SAMPLES





#Prediction Func
def predict(input):
    model = tf.keras.models.load_model("/Users/rahulfernandes/Projects/Iot Based System to Detect Sleep Apnea using Deep Learning/ML_Traning/Models/85.71/sleep_apnea_model_8571.h5")
    #model.summary()
    #for layer in model.layers:
    #    print(layer.input_shape)
    
    test_data = tf.convert_to_tensor(input.reshape(1,2560000,1,1))


    prediction = model.predict(test_data,verbose=0)
    return CATEGORIES[int(prediction[0][0])]
    





#Pre-Processing Function
def processing(file_path,samples):
    
    contents = pd.read_csv(file_path,nrows=samples)
    
    ecg_data = contents['ECG']
    #print(ecg_data)
    filtered_signal = filter(np.array(ecg_data))
    normfilt_signal = normalise_signal(np.array(filtered_signal))
    return normfilt_signal
    
   



#High Pass Filter
def filter(ecg_signal):
    
    #4th Order Butterworth Highpass Filter at 0.5Hz
    highpass = 0.5
    nyq = 0.5 * SAMPLE_FREQUENCY
    cutoff = highpass / nyq
    order = 4

    b, a = scipy.signal.butter(order, cutoff, btype='highpass', analog=False)
    y = scipy.signal.filtfilt(b, a, ecg_signal, axis=-1)
    
    return (y)

#Z-Score Normalisation
def normalise_signal(ecg_signal):
    mean = ecg_signal.mean()
    std = ecg_signal.std()
    normalised_signal = []

    for voltage in np.nditer(ecg_signal):
        normalised_signal.append((
            (voltage - mean) / std
        ))
    return np.array(normalised_signal)

