# SAR影像特征匹配系统

这是一个用于SAR（合成孔径雷达）影像特征匹配的图形界面应用程序。该系统支持多种特征匹配算法，可以处理多种图像格式，包括TIFF格式的SAR影像。

## 功能特点

- 支持多种图像格式（TIFF, JPEG, PNG, BMP等）
- 提供多种特征匹配算法：
  - BRISK (Binary Robust Invariant Scalable Keypoints)
  - ORB (Oriented FAST and Rotated BRIEF)
  - SIFT (Scale-Invariant Feature Transform)
  - AKAZE (Accelerated-KAZE)
- 图形用户界面，操作简单直观
- 实时显示匹配结果

## 系统要求

- Python 3.x
- 依赖库：
  - OpenCV (cv2)
  - NumPy
  - Tkinter (Python内置)
  - Pillow (PIL)

## 安装依赖

```bash
pip install opencv-python
pip install numpy
pip install pillow
```

## 使用说明

1. 运行程序：
   ```bash
   python python.py
   ```

2. 操作步骤：
   - 从下拉菜单选择特征匹配算法（BRISK、ORB、SIFT或AKAZE）
   - 点击"选择第一个图片"按钮选择第一张图片
   - 点击"选择第二个图片"按钮选择第二张图片
   - 点击"开始匹配"按钮进行特征匹配
   - 按ESC键或'q'键关闭匹配结果窗口

## 注意事项

- 支持的图像格式包括：.tif, .tiff, .jpg, .jpeg, .png, .bmp
- TIFF格式图像会自动转换为灰度图像进行处理
- 匹配结果窗口可以调整大小以便查看细节

## 作者信息

- 一个苦逼的中国大学生罢了
