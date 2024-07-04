import cv2
import numpy 

def nothing(x):
    pass

def camera_undistort(image, mtx, dist):
    width, height = image.shape[:2]
    
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(
        mtx, dist, (width,height), 0.01, (width,height))
    distort_image = cv2.undistort(image, mtx, dist, newcameramtx)
    
    return distort_image

def select(image, mtx, dist):
    cv2.namedWindow('image')
    cx, cy = int(mtx[0][0]), int(mtx[1][1])
    x0, y0 = int(mtx[0][2]), int(mtx[1][2])
    p1, p2, k1, k2, p3 = dist[0]

    cv2.createTrackbar('P1', 'image', 0, 100000, nothing)
    cv2.createTrackbar('P2', 'image', 0, 100000, nothing)
    cv2.createTrackbar('P3', 'image', 0, 100000, nothing)
    cv2.createTrackbar('K1', 'image', 0, 100000, nothing)
    cv2.createTrackbar('K2', 'image', 0, 100000, nothing)
    cv2.createTrackbar('CX', 'image', 0, 3000, nothing)
    cv2.createTrackbar('CY', 'image', 0, 3000, nothing)
    cv2.createTrackbar('X0', 'image', 0, image.shape[1], nothing)
    cv2.createTrackbar('Y0', 'image', 0, image.shape[0], nothing)

    cv2.setTrackbarPos('P1', 'image', 50000)
    cv2.setTrackbarPos('P2', 'image', 50000)
    cv2.setTrackbarPos('P3', 'image', 50000)
    cv2.setTrackbarPos('K1', 'image', 50000)
    cv2.setTrackbarPos('K2', 'image', 50000) 
    cv2.setTrackbarPos('CX', 'image', cx) 
    cv2.setTrackbarPos('CY', 'image', cy) 
    cv2.setTrackbarPos('X0', 'image', x0) 
    cv2.setTrackbarPos('Y0', 'image', y0) 
    
    while(1):   
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break
        p1_n = (cv2.getTrackbarPos('P1', 'image')-50000)/100000. + p1
        p2_n = (cv2.getTrackbarPos('P2', 'image')-50000)/100000. + p2
        p3_n = (cv2.getTrackbarPos('P3', 'image')-50000)/100000. + p3
        k1_n = (cv2.getTrackbarPos('K1', 'image')-50000)/100000. + k1
        k2_n = (cv2.getTrackbarPos('K2', 'image')-50000)/100000. + k2
        cx_n = cv2.getTrackbarPos('CX', 'image')
        cy_n = cv2.getTrackbarPos('CY', 'image')
        x0_n = cv2.getTrackbarPos('X0', 'image')
        y0_n = cv2.getTrackbarPos('Y0', 'image')

        mtx[0][0], mtx[1][1] = cx_n, cy_n
        mtx[0][2], mtx[1][2] = x0_n, y0_n
        dist = numpy.array([[p1_n, p2_n, k1_n, k2_n, p3_n]])

        show_image = camera_undistort(image, mtx, dist)
        show_image = cv2.resize(show_image, (960, 540))
        show_image = cv2.putText(show_image, f'mtx: [[{cx_n:<5}, 0.000, {x0_n:<5}] ', (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        show_image = cv2.putText(show_image, f'      [0.000, {cy_n:<5}, {y0_n:<5}] ', (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        show_image = cv2.putText(show_image, f'      [0.000, 0.000, 1.000]]', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        
        show_image = cv2.putText(show_image, f'P1: {p1_n}, P2: {p2_n}, P3: {p3_n}, K1: {k1_n}, K2: {k2_n}', 
                                 (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        cv2.imshow('image', show_image)

    cv2.destroyAllWindows()

if __name__ == '__main__':
    oriimage = cv2.imread('image.png')
    orimtx = numpy.array(
        [[1.43827717e+03, 0.00000000e+00, 1.2899408e+03],
         [0.00000000e+00, 1.45446044e+03, 7.28118878e+02],
         [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])
    oridist = numpy.array([[-0.23607527, -0.07857215, -0.00030963, 0.00040639, 0.11326096]])
    
    select(oriimage, orimtx, oridist)