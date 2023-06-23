from tensorflow.keras.models import load_model
from keras_vggface.utils import preprocess_input
from keras_vggface.vggface import VGGFace
import tensorflow as tf
import numpy as np
import os
import pickle
import cv2
from sklearn.metrics.pairwise import cosine_similarity
import cv2
from mtcnn import MTCNN
from PIL import Image

feature_list = np.array(pickle.load(open('embedding.pkl','rb')))
filenames = pickle.load(open('filenames.pkl','rb'))


model = load_model('my_vgg16.h5')

detector = MTCNN()
# load img -> face detection
sample_img = cv2.imread('fake5.jpg')
results = detector.detect_faces(sample_img)

x,y,width,height = results[0]['box']

face = sample_img[y:y+height,x:x+width]

#  extract its features
image = Image.fromarray(face)
image = image.resize((224,224))

face_array = np.asarray(image)

face_array = face_array.astype('float32')

expanded_img = np.expand_dims(face_array,axis=0)
preprocessed_img = preprocess_input(expanded_img)
result = model.predict(preprocessed_img).flatten()

similarity = []
for i in range(len(feature_list)):
    similarity.append(cosine_similarity(result.reshape(1,-1),feature_list[i].reshape(1,-1))[0][0])

index_pos = sorted(list(enumerate(similarity)),reverse=True,key=lambda x:x[1])[0][0]

print(filenames[index_pos])
temp_img = cv2.imread(filenames[index_pos])

print(filenames[index_pos]) 
cv2.imshow('output',temp_img)

cv2.waitKey(0)