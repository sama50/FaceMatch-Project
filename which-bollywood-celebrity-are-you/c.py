import tensorflow as tf
converter = tf.lite.TFLiteConverter.from_saved_model('my_vgg16.h5')
tflite_model = converter.convert()