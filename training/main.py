import os
import glob
import numpy as np
import librosa
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from sklearn.model_selection import train_test_split

# 1. Extração de MFCC
def extract_mfcc(file_path, max_len=32):
    audio, sr = librosa.load(file_path, sr=16000)
    mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=13)
    if mfcc.shape[1] < max_len:
        pad_width = max_len - mfcc.shape[1]
        mfcc = np.pad(mfcc, pad_width=((0, 0), (0, pad_width)), mode='constant')
    else:
        mfcc = mfcc[:, :max_len]
    return mfcc

# 2. Carregar dados e extrair MFCC
X = []
y = []

labels = {'on': 0, 'off': 1, '_background_noise_': 2}

dataset_path = 'dataset'  # ajuste conforme necessário
for label in labels:
    files = glob.glob(os.path.join(dataset_path, label, '*.wav'))
    for f in files:
        mfcc = extract_mfcc(f)
        X.append(mfcc)
        y.append(labels[label])

X = np.array(X)
y = np.array(y)
X = X[..., np.newaxis]  # adiciona canal para CNN

# 3. Divisão treino/validação
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Definir e treinar modelo
model = Sequential([
    Conv2D(16, (3, 3), activation='relu', input_shape=X.shape[1:]),
    MaxPooling2D((2, 2)),
    Flatten(),
    Dense(64, activation='relu'),
    Dense(3, activation='softmax')
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_val, y_val))
model.save("model.hdf5")

# 5. Converter para TFLite e salvar como model.h
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

with open("model.h5", "w") as file:
    array = ", ".join(str(b) for b in tflite_model)
    file.write(f"const unsigned char model[] = {{{array}}};\n")
    file.write(f"const int model_len = {len(tflite_model)};\n")