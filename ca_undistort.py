import os
import cv2
import numpy

def camera_undistort(image, mtx, dist, is_show):
    width, height = image.shape[:2]
    
    if is_show:
        origin_image = cv2.resize(image, (960, 540))
        cv2.imshow('1', origin_image)
        cv2.waitKey(0)

    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (width,height), 0.01, (width,height))
    dst_image = cv2.undistort(image, mtx, dist, newcameramtx)
    
    if is_show:
        show_image = cv2.resize(dst_image, (960, 540))
        cv2.imshow('1', show_image)
        cv2.waitKey(0)
    
    return dst_image

if __name__ == '__main__':
    image = cv2.imread('sample.jpg')

    mtx = numpy.array(
        [[1.43827717e+03, 0.00000000e+00, 1.00899408e+03],
         [0.00000000e+00, 1.45446044e+03, 5.28118878e+02],
         [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])
    dist = numpy.array([[-0.23607527, -0.17857215, -0.00030963, 0.00040639, 0.21326096]])

    dst_image = camera_undistort(image, mtx, dist, is_show = True)