from keras_vggface.utils import preprocess_input
from keras_vggface.vggface import VGGFace
import tensorflow as tf
import numpy as np
import pickle
from sklearn.metrics.pairwise import cosine_similarity
import cv2
from mtcnn import MTCNN
from PIL import Image

feature_list = np.array(pickle.load(open('embedding.pkl','rb')))
filenames = pickle.load(open('filenames.pkl','rb'))

model = VGGFace(model='resnet50',include_top=False,input_shape=(224,224,3),pooling='avg')

detector = MTCNN()
# load img -> face detection
sample_img = cv2.imread('fake.jpg')
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
#print(result)
#print(result.shape)
# find the cosine distance of current image with all the 8655 features
similarity = []
for i in range(len(feature_list)):
    similarity.append(cosine_similarity(result.reshape(1,-1),feature_list[i].reshape(1,-1))[0][0])

index_pos = sorted(list(enumerate(similarity)),reverse=True,key=lambda x:x[1])[0][0]
# index_pos1 = sorted(list(enumerate(similarity)),reverse=True,key=lambda x:x[1])[1][0]
# index_pos2 = sorted(list(enumerate(similarity)),reverse=True,key=lambda x:x[1])[2][0]
# index_pos3 = sorted(list(enumerate(similarity)),reverse=True,key=lambda x:x[1])[3][0]

temp_img = cv2.imread(filenames[index_pos])
# temp_img1 = cv2.imread(filenames[index_pos1])
# temp_img2 = cv2.imread(filenames[index_pos2])
# temp_img3 = cv2.imread(filenames[index_pos3])
print(filenames[index_pos]) 
cv2.imshow('output',temp_img)
# cv2.imshow('output1',temp_img1)
# cv2.imshow('output2',temp_img2)
# cv2.imshow('output3',temp_img3)
cv2.waitKey(0)
# recommend that image


# https://www.kaggle.com/datasets/vishesh1412/celebrity-face-image-dataset
# https://www.kaggle.com/datasets/sushilyadav1998/bollywood-celeb-localized-face-dataset?resource=download
# https://drive.google.com/drive/folders/0B5G8pYUQMNZnLTBVaENWUWdzR0E?resourcekey=0-gRGzioHdCR4zkegs6t1W2Q