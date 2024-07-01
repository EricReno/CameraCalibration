import os
import cv2
import glob
import numpy as np

def camera_calibration(images_dir, is_show, image_size):
    objps = np.zeros((5*9, 3), np.float32)
    objps[:, :2] = np.mgrid[0:5, 0:9].T.reshape(-1, 2)
    
    objpoints, imgpoints = [], []
    images_list = glob.glob(os.path.join(images_dir, '*.jpg'))

    for image_path in images_list:
        img = cv2.imread(image_path)
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        if is_show:
            cv2.imshow('img', gray)
            cv2.waitKey(0)

        ret, corners = cv2.findChessboardCorners(img, (5, 9), None)
        if not ret:
            print(image_path, ret)
        else:
            corners = cv2.cornerSubPix(gray, corners, (6, 10), (-1, -1),
                                       criteria=(cv2.TERM_CRITERIA_EPS+cv2.TermCriteria_MAX_ITER, 30, 0.001))
            cv2.drawChessboardCorners(img, (5,9), corners, ret)
            objpoints.append(objps)
            imgpoints.append(corners)

            if is_show:
                cv2.imshow('img', img)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, imageSize=image_size, cameraMatrix=None, distCoeffs=None)
    
    return mtx, dist
    
if __name__ == "__main__":
    mtx, dist = camera_calibration(
                                os.path.join(os.getcwd(), 'images'), 
                                is_show = False,
                                image_size = (1920, 1080)
                                )
    print(mtx, dist)