import os
import numpy as np      #version 1.19.5
import PIL.Image        #version 7.1.2
import cv2              #version 4.1.2
from tensorflow import keras    #version 2.7.0
from tensorflow.keras.preprocessing.image import load_img
from skimage.feature import hog #verison 0.18.3
from PIL import Image


class Model:

  def __init__(self):
    self.img_size = (256,256)
    self.seg_model = keras.models.load_model('resources/models/tomato.h5', custom_objects={"dice_coef": self.dice_coef, "iou_coef":self.iou_coef})
    self.class_model = keras.models.load_model('resources/models/mixed_best_model0.hdf5', custom_objects={"recall": self.recall, "precision":self.precision})


  def dice_coef(self, y_true, y_pred, smooth=1):

    intersection = K.sum(y_true * y_pred, axis=[1,2,3])
    union = K.sum(y_true, axis=[1,2,3]) + K.sum(y_pred, axis=[1,2,3])
    dice = K.mean((2. * intersection + smooth)/(union + smooth), axis=0)

    return dice


  def iou_coef(self, y_true, y_pred, smooth=1):

    intersection = K.sum(K.abs(y_true * y_pred), axis=[1,2,3])
    union = K.sum(y_true,[1,2,3])+K.sum(y_pred,[1,2,3])-intersection
    iou = K.mean((intersection + smooth) / (union + smooth), axis=0)

    return iou


  def precision(self, y_true, y_pred): #taken from old keras source code

    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + K.epsilon())

    return precision


  def recall(self, y_true, y_pred): #taken from old keras source code

    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    recall = true_positives / (possible_positives + K.epsilon())
    
    return recall


  def classify(self, Pic_Path):

    img = load_img(Pic_Path, target_size=self.img_size)
    x = np.zeros((1,) + self.img_size + (3,), dtype="float32")
    x[0] = img
    mask = self.seg_model.predict(x)
    mask = np.argmax(mask, axis=-1)
    img_new = cv2.imread(Pic_Path)
    result = img_new.copy()
    result[mask[0] == 0] = 0
    cv2.imwrite("images/temp.png",result)

    img = Image.open("images/temp.png")

    hog_in = np.array(img)
    fd, hog_image = hog(hog_in,orientations=9, pixels_per_cell=(8, 8),cells_per_block=(2, 2), visualize=True, multichannel=True)
    x1 = np.zeros((1,) + self.img_size + (3,), dtype="float32")
    x2 = np.zeros((1,) + (34596,) , dtype="float32")
    x1[0] = img
    x2[0] = fd
    pred = self.class_model.predict([x2,x1])
    val = np.argmax(pred,axis=1)

    output = ""
    if(val == 0):
      output = "disease 09"
    elif(val == 1):
      output = "disease 08"
    elif(val == 2):
      output = "disease 07"
    elif(val == 3):
      output = "disease 06"
    elif(val == 4):
      output = "disease 05"
    elif(val == 5):
      output = "disease 04"
    elif(val == 6):
      output = "disease 03"
    elif(val == 7):
      output = "disease 01"
    elif(val == 8):
      output = "disease 02"
    elif(val == 9):
      output = "disease 00"

    return output


if __name__ == "__main__":
  model = Model()
  print(model.classify('images/d1641031959414.jpg'))
