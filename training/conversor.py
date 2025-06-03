import tensorflow as tf

# Carrega o modelo Keras
model = tf.keras.models.load_model("model.hdf5")

# Converte para TFLite
converter = tf.lite.TFLiteConverter.from_keras_model(model)
# (opcional) Otimizações para modelos pequenos
converter.optimizations = [tf.lite.Optimize.DEFAULT]

# Gera modelo .tflite
tflite_model = converter.convert()

# Salva em disco
with open("model.tflite", "wb") as f:
    f.write(tflite_model)

print("Modelo TFLite salvo como model.tflite")
