import cv2
import numpy
from ca_undistort import camera_undistort

from matplotlib import pyplot as plt

def bev_convert(image, pt_pixel, pt_world, is_show):
    height, width = image.shape[:2]
    area_x = max(pt_world[:, 0]) - min(pt_world[:, 0]) + 100
    area_y = max(pt_world[:, 1]) - min(pt_world[:, 1]) + 100

    M, mask = cv2.findHomography(pt_pixel, pt_world)

    ## 逆透视变换到BEV
    transformed_image = cv2.warpPerspective(image, M, (image.shape[1], image.shape[0]))
    padded_image = numpy.zeros((height, width, 3), dtype=numpy.uint8)
    padded_image[int((height-area_y)//2):int((height+area_y)//2), 
                 int((width-area_x)//2):int((width+area_x)//2), 
                 :
                ] = transformed_image[
                                      int(min(pt_world[:, 1])):int(max(pt_world[:, 1])+100),
                                      int(min(pt_world[:, 0])):int(max(pt_world[:, 0])+100), 
                                      :
                                     ]
    
    if is_show:
        show_image = cv2.resize(transformed_image, (width//2, height//2))
        cv2.imshow('1', show_image)
        cv2.waitKey(0)

        show_image = cv2.resize(padded_image, (width//2, height//2))
        cv2.imshow('1', show_image)
        cv2.waitKey(0)
    
    return padded_image
    
if __name__ == "__main__":
    is_show=True
    image = cv2.imread('sample.jpg')

    ## 获取dst图像
    mtx = numpy.array(
        [[1.43827717e+03, 0.00000000e+00, 1.00899408e+03],
         [0.00000000e+00, 1.45446044e+03, 5.28118878e+02],
         [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])
    dist = numpy.array([[-0.23607527, -0.17857215, -0.00030963, 0.00040639, 0.21326096]])
    dst_image = camera_undistort(image, mtx, dist, is_show)

    ## 获取配准点
    pt_pixel = numpy.float32([[ 314, 294], [ 526, 1047], [1759, 834], [1518,  598]])
    pt_world = numpy.float32([[ 600, 900], [1000,  900], [1000, 100], [ 600,  100]])
    
    padded_image = bev_convert(dst_image, pt_pixel, pt_world, is_show)