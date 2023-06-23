# !pip install mtcnn==0.1.0
# !pip install tensorflow==2.3.1
# !pip install keras==2.4.3
# !pip install keras-vggface==0.6
# !pip install keras_applications==1.0.8

# import os
# import pickle 
 
# filenames = []

# actors = os.listdir('data')

# filenames = []

# for actor in actors:
#     for file in os.listdir(os.path.join('data',actor)):
#         filenames.append(os.path.join('data',actor,file))
 
# pickle.dump(filenames,open('filenames.pkl','wb'))

import tensorflow
import keras
from tensorflow.keras.preprocessing import image
from keras_vggface.utils import preprocess_input
from keras_vggface.vggface import VGGFace
import numpy as np
import pickle
from tqdm import tqdm 
print(tensorflow.__version__)
print(keras.__version__)
filenames = pickle.load(open('filenames.pkl','rb')) 
print(filenames[0])
model = VGGFace(model='resnet50',include_top=False,input_shape=(224,224,3),pooling='avg')

def feature_extractor(img_path,model):
    print(img_path)
    img = image.load_img(img_path,target_size=(224,224))
    img_array = image.img_to_array(img)
    expanded_img = np.expand_dims(img_array,axis=0)
    preprocessed_img = preprocess_input(expanded_img)

    result = model.predict(preprocessed_img).flatten()

    return result

features = []
i =0
for file in tqdm(filenames):
   
    features.append(feature_extractor(file,model))
    
print(features)
pickle.dump(features,open('embedding.pkl','wb'))

model.save('my_vgg16.h5')