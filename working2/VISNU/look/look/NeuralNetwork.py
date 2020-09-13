import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import os, os.path
import cv2

# --- Défintion des fonctions ---

def imread(path):
    im = cv2.imread(path)
    im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    im = cv2.threshold(im, 128, 255, cv2.THRESH_BINARY)[1]
    im = im / 255
    im = np.asarray(im).flatten()
    return im

def get_prediction_result(tensor):
    max_value = 0
    index = 0
    for i in range(len(tensor)):
        if(tensor[i]) > max_value:
            max_value = tensor[i]
            index = i
    return index

# --- Lecture des Fichiers ---

path = './look/Datas/'
X_list = []
Y_list = []

for i in range(10):
    filenames = os.listdir(path + str(i))
    filenames.sort()
    for n, fi in enumerate(filenames):
        path_to_img = path+str(i)+'/'+fi
        tab_im = imread(path_to_img)
        X_list.append(tab_im)
        Y_list.append(i)

X = np.array(X_list).reshape(-1, 20, 20)
Y = np.array(Y_list)

# --- Partie NN ---

model = tf.keras.models.Sequential([
        tf.keras.layers.Flatten(input_shape=(20,20)),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(10, activation='softmax')
])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
model.fit(X, Y, epochs=200)

# --- Partie Production ---

# Lecture d'une images
X_testing = []
test_image8 = imread("temp.png")
X_testing.append(test_image8)

#Prédiction des résultats
X_testing_final = np.array(X_testing).reshape(-1,20,20)
result_tensor = model.predict(X_testing_final)
prediction = get_prediction_result(result_tensor[0]) # @Kenett : prediction contient la valeur prédite à envoyer
print(prediction)

def Return_Prediction():
        return prediction

file = open('{a}.txt'.format(a = "prediction"),"w")
file.write("%s" % prediction)
file.close()

