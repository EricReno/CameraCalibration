# CameraCalibration

## 相机标定算法的简单应用

- **ca_calibrate**: 相机标定，计算相机的内参矩阵和畸变参数

- **ca_undistort**: 根据相机内参和畸变参数，对图像进行畸变矫正

- **ca_bev**: 根据配准计算相机外参（单映性矩阵），对图像进行投影变换，生成BEV图

- **main**: 手动调节内参与畸变函数

- **进阶版--AVM环视拼接方法**：https://mp.weixin.qq.com/s/CZR2iIMrlHgmihoqncuciA