from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from rest_framework.decorators import api_view
from rest_framework.response import Response
from app.serializers import ImageSerializer
from app.models import SaveImage
from tensorflow.keras.models import load_model
from keras_vggface.utils import preprocess_input
from keras_vggface.vggface import VGGFace
import tensorflow as tf
import os
from django.core.files import File
import numpy as np
import pickle
from sklearn.metrics.pairwise import cosine_similarity
import cv2
from mtcnn import MTCNN
from PIL import Image

feature_list = np.array(pickle.load(open('app//embedding.pkl','rb')))
filenames = pickle.load(open('app//filenames.pkl','rb'))
model = load_model('app//my_vgg16.h5')

detector = MTCNN() 

@api_view(['POST'])
def upload_image(request): 
    print("*** Uploading image")
    serializer = ImageSerializer(data=request.data)
    if serializer.is_valid():
        # Process the image file as needed
        try:
            image = serializer.validated_data['image']
            # Save the image to a location accessible by the frontend
            file_name = default_storage.save(image.name, ContentFile(image.read()))
            image_url = settings.MEDIA_URL + file_name
            file = SaveImage(comeing_img=image)
            file.save()
            # image_url = request.build_absolute_uri(file.comeing_img.url)
            # print(image_url)
            sample_img = cv2.imread(file.comeing_img.path)
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
            print(index_pos)
            print("***********")
            print(index_pos)
        
            print("################################")
        
            image_url = ''
            image_path = 'app\\'+filenames[int(index_pos)]
            print(filenames[int(index_pos)])
            with open(image_path, 'rb') as img_file:
                file.output_img = File(img_file)
                file.save()
                print(file.output_img)
                image_url = request.build_absolute_uri(file.output_img.url)
                print(image_url)
            # Return the image URL in the response
            name = filenames[int(index_pos)].split('\\')[1]
            print(name)
            return Response({'image_url': image_url ,'name':name, 'message': 'Image uploaded successfully'})
        except Exception as e:
            print(e)
    else:
        # Return an error response
        return Response(serializer.errors, status=400)
