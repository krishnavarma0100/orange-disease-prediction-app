import os
import cv2
import numpy as np
import skimage
from keras.preprocessing.image import ImageDataGenerator

IMAGE_SIZE=256
BATCH_SIZE=32

class IMAGE_PREPROCESSING:

    def __init__(self,path) -> None:
        self.path=path

    def preprocess_function(img):

        # Brighthness and contrast (Enhancement)
        alpha = 1.17
        beta = 5
        cont_bright = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)

        # Noise Removal (Gaussian Filtering)
        Gaussian = cv2.GaussianBlur(cont_bright, (3, 3), 0)

        # Sharp Image
        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
        sharpened_image = cv2.filter2D(Gaussian, -1, kernel)

        # Histogram Equalization
        img_yuv = cv2.cvtColor(sharpened_image,cv2.COLOR_BGR2YUV)
        img_yuv[:,:,0] = cv2.equalizeHist(img_yuv[:,:,0])
        hist_eq = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)

        image=skimage.img_as_float(hist_eq)
        return image
    
    def PreprocessImage(self,disease_folder_names):
        
        datagen=ImageDataGenerator(
            preprocessing_function=IMAGE_PREPROCESSING.preprocess_function,
        )

        if(os.path.isdir(self.path)):

            dataset_generator=datagen.flow_from_directory(
                self.path,
                target_size=(IMAGE_SIZE,IMAGE_SIZE),
                batch_size=BATCH_SIZE,
                shuffle=True,
                class_mode='sparse',
                classes=disease_folder_names
            )
            
            return dataset_generator
            
        else:

            im=self.path
            im=cv2.resize(im,(256,256))
            lst=[im]
            image=np.array(lst)
            dataset_generator=datagen.flow(
                image,
                batch_size=1,
            )
        
            return dataset_generator