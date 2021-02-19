import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
from PIL import Image 
import os
import tensorflow as tf 
import tensorflow.keras as keras
from tensorflow.keras import Sequential,Model 
from tensorflow.keras.layers import Conv2D, Flatten, MaxPooling2D,Dense,Dropout,Input
from tensorflow.keras.applications import InceptionV3
 
config = tf.compat.v1.ConfigProto()
config.gpu_options.per_process_gpu_memory_fraction = 0.7
session = tf.compat.v1.Session(config=config)

basewidth = 240

max_size = 4000
classes = os.listdir("../classes")
one_hot_vector = np.zeros((1,len(classes)))

train_data_x = np.zeros((max_size,180,basewidth,3))
train_data_y = np.zeros((max_size,len(classes)))

test_data_x = np.zeros((max_size,180,basewidth,3))
test_data_y = np.zeros((max_size,len(classes)))

count_training = 0
count_test = 0
vec = []
for class_element in classes :
    i = int(class_element.replace("class_","")) - 1
    print(i)
    images = os.listdir("../classes/"+class_element+"/spectro/")
    split_train = int(0.7*len(images))
    split_test = len(images)-split_train
    part_counter = 0
    print("==========================================================")
    for image in images :
        print(image)
        if image[0] != "a" :
            img = Image.open("../classes/"+class_element+"/spectro/"+image)
            img.load()
            img = img.convert('RGB')
            wpercent = (basewidth/float(img.size[0]))
            hsize = 180
            img = img.resize((240,hsize), Image.ANTIALIAS)
            data = np.asarray(img, dtype="float32")
            if part_counter < split_train :
                train_data_x[count_training,:,:,:] = data 
                train_data_y[count_training,i] = 1 
                count_training = count_training + 1
                part_counter = part_counter + 1
                list_augment = os.listdir("../classes/"+class_element+'/spectro/augment/')
                print("==========================================================")
                for spec in list_augment :
                    try :
                        if  int(spec[:3]) == int(image.replace(".png","")) :
                            print(spec)
                            img = Image.open("../classes/"+class_element+"/spectro/augment/"+spec)
                            img.load()
                            img = img.convert('RGB')
                            wpercent = (basewidth/float(img.size[0]))
                            hsize = 180
                            img = img.resize((240,hsize), Image.ANTIALIAS)
                            data = np.asarray(img, dtype="float32")
                            train_data_x[count_training,:,:,:] = data 
                            train_data_y[count_training,i] = 1 
                            count_training = count_training + 1
                        else :
                            pass
                    except Exception as e :
                        try :
                            if  int(spec[:2]) == int(image.replace(".png","")) :
                                print(spec)
                                img = Image.open("../classes/"+class_element+"/spectro/augment/"+spec)
                                img.load()
                                img = img.convert('RGB')
                                wpercent = (basewidth/float(img.size[0]))
                                hsize = 180
                                img = img.resize((240,hsize), Image.ANTIALIAS)
                                data = np.asarray(img, dtype="float32")
                                train_data_x[count_training,:,:,:] = data 
                                train_data_y[count_training,i] = 1 
                                count_training = count_training + 1
                        except Exception as e :
                            if  int(spec[:1]) == int(image.replace(".png","")) :
                                print(spec)
                                img = Image.open("../classes/"+class_element+"/spectro/augment/"+spec)
                                img.load()
                                img = img.convert('RGB')
                                wpercent = (basewidth/float(img.size[0]))
                                hsize = 180
                                img = img.resize((240,hsize), Image.ANTIALIAS)
                                data = np.asarray(img, dtype="float32")
                                train_data_x[count_training,:,:,:] = data 
                                train_data_y[count_training,i] = 1 
                                count_training = count_t
            else :
                test_data_x[count_test,:,:,:] = data 
                test_data_y[count_test,i] = 1 
                count_test = count_test + 1
                vec.append(int(image.replace(".png","")))
            


train_data_x = train_data_x[: count_training,:,:,:]
train_data_y = train_data_y[: count_training,:]

test_data_x = test_data_x[: count_test,:,:,:]
test_data_y = test_data_y[: count_test,:]


with open('train_data_x.npy', 'wb') as f:
    np.save(f, train_data_x)

with open('train_data_y.npy', 'wb') as f1:
    np.save(f1, train_data_y)

with open('test_data_x.npy', 'wb') as f2:
    np.save(f2, test_data_x)

with open('test_data_y.npy', 'wb') as f3:
    np.save(f3, test_data_y)


train_data_y = np.load("./train_data_y.npy").astype('float32')
train_data_x = np.load("./train_data_x.npy").astype('float32')
train_data_x /= 255 
test_data_x = np.load("./test_data_x.npy").astype('float32')
test_data_x /= 255
test_data_y = np.load("./test_data_y.npy").astype('float32')



input=Input(shape=(180, 240, 3))
classifier = InceptionV3(include_top=False ,weights='imagenet')(input)
top_model = Flatten()(classifier)
top_model = Dense(2046,activation="relu") (top_model)
top_model = Dense(1024,activation="relu") (top_model)
top_model = Dense(512,activation="relu") (top_model)
output = Dense(18,activation='softmax') (top_model)
classifier=Model(input,output)
classifier.compile(optimizer='adam',loss='categorical_crossentropy',metrics=['accuracy'])

classifier.fit(train_data_x, train_data_y,
                    batch_size=7,
                    epochs=17)

results = classifier.evaluate(test_data_x, test_data_y, batch_size=7)
print('test loss, test acc:', results)


#Sauvegarde du modele
classifier.save('model2.h5')