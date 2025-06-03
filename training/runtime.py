import os
import numpy as np
import librosa
import tensorflow as tf

# === 1. Caminho do modelo e do áudio ===
MODEL_PATH = "model.tflite"
AUDIO_PATH = "dataset/on/0a7c2a8d_nohash_0.wav"  # Troque por outro se quiser

# === 2. Carrega e processa o áudio ===
y, sr = librosa.load(AUDIO_PATH, sr=16000)
y = y[:16000]  # garante exatamente 1 segundo

# Extrai MFCCs (ex: 13 coeficientes, 32 quadros)
mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
mfcc = mfcc[:, :32]  # garante formato (13, 32)
if mfcc.shape[1] < 32:
    pad_width = 32 - mfcc.shape[1]
    mfcc = np.pad(mfcc, ((0, 0), (0, pad_width)), mode='constant')

# Normaliza e formata para modelo TFLite
input_data = mfcc[np.newaxis, ..., np.newaxis].astype(np.float32)  # (1, 13, 32, 1)

# === 3. Carrega modelo TFLite ===
interpreter = tf.lite.Interpreter(model_path=MODEL_PATH)
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# === 4. Inferência ===
interpreter.set_tensor(input_details[0]['index'], input_data)
interpreter.invoke()
output = interpreter.get_tensor(output_details[0]['index'])

# === 5. Resultado ===
predicted_class = np.argmax(output)
confidence = output[0][predicted_class]

print(f"Classe predita: {predicted_class} (Confiança: {confidence:.2f})")
