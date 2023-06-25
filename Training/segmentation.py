import cv2
import numpy as np
import matplotlib.pyplot as plt


class IMAGE_SEGMENTATION:
    
    def __init__(self,image) -> None:
        self.image=image

    def AnalyzeImage(self):
        filtered_image = cv2.GaussianBlur(self.image, (3, 3), 0)
        img_lab = cv2.cvtColor(filtered_image, cv2.COLOR_RGB2LAB)  
        img_hsv = cv2.cvtColor(filtered_image, cv2.COLOR_RGB2HSV)

        # Lab Channel
        L = img_lab[:, :, 0]
        a = img_lab[:, :, 1]
        b = img_lab[:, :, 2]
        # fig, ax = plt.subplots(1,3, figsize=(15,4))
        # ax[0].imshow(L)
        # ax[1].imshow(a)
        # ax[2].imshow(b)
        # fig.suptitle("Lab")
        # plt.show()

        # HSV Channel
        H = img_hsv[:, :, 0]
        S = img_hsv[:, :, 1]
        V = img_hsv[:, :, 2]
        # fig, ax = plt.subplots(1,3, figsize=(15,4))
        # ax[0].imshow(H)
        # ax[1].imshow(S)
        # ax[2].imshow(V)
        # fig.suptitle("HSV")
        # plt.show()


        pixel_vals = b.flatten()
        pixel_vals = np.float32(pixel_vals)
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)

        # Forming the clusters
        K = 2
        retval, labels, centers = cv2.kmeans(pixel_vals, K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        centers = np.uint8(centers)
        segmented_data = centers[labels.flatten()]
        segmented_image = segmented_data.reshape((b.shape))

        mask1=np.where(segmented_image==segmented_image[0][0],0,1)
        # fig, ax = plt.subplots(1,3, figsize=(15,4))
        # ax[0].imshow(mask1)


        # Masking with HSV value
        low=np.array([0,25,23])
        high=np.array([50,255,255])
        mask2=cv2.inRange(img_hsv,low,high)
        mask2=(mask2/255).astype("int32")
        # ax[1].imshow(mask2)

        # Bitwise or between two masks
        mask=cv2.bitwise_or(mask1,mask2)
        # ax[2].imshow(mask)

        return mask

    def Segmentation(self,mask):

        R = self.image[:, :, 0]
        G = self.image[:, :, 1]
        B = self.image[:, :, 2]

        # Extract only masked pixels
        r = R*mask
        g = G*mask
        b = B*mask
        final_img = np.dstack((r, g, b))

        return final_img