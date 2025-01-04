import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import Image

# 初始化Tkinter窗口
root = tk.Tk()

# 选择第一张图片
def select_first_image():
    global img1, keypoints1, descriptors1
    file_path1 = filedialog.askopenfilename(filetypes=[("Image files", "*.tif *.tiff *.jpg *.jpeg *.png *.bmp")])
    if file_path1:
        # Check if file is TIFF
        if file_path1.lower().endswith(('.tif', '.tiff')):
            try:
                # Use Pillow to load TIFF
                pil_img = Image.open(file_path1).convert('L')  # Convert to grayscale
                img1 = np.array(pil_img)  # Convert to numpy array
            except Exception as e:
                label.config(text=f"无法加载TIFF图片: {file_path1}\n错误: {str(e)}")
                return
        else:
            img1 = cv2.imread(file_path1, 0)  # 0表示以灰度模式读取
            if img1 is None:
                label.config(text=f"无法加载图片: {file_path1}\n请检查文件路径和格式")
                return
        
        # 使用ORB检测关键点和描述符
        orb = cv2.ORB_create()
        keypoints1, descriptors1 = orb.detectAndCompute(img1, None)
        show_image(img1, "Image 1")

# 选择第二张图片
def select_second_image():
    global img2, keypoints2, descriptors2
    file_path2 = filedialog.askopenfilename(filetypes=[("Image files", "*.tif *.tiff *.jpg *.jpeg *.png *.bmp")])
    if file_path2:
        # Check if file is TIFF
        if file_path2.lower().endswith(('.tif', '.tiff')):
            try:
                # Use Pillow to load TIFF
                pil_img = Image.open(file_path2).convert('L')  # Convert to grayscale
                img2 = np.array(pil_img)  # Convert to numpy array
            except Exception as e:
                label.config(text=f"无法加载TIFF图片: {file_path2}\n错误: {str(e)}")
                return
        else:
            img2 = cv2.imread(file_path2, 0)
            if img2 is None:
                label.config(text=f"无法加载图片: {file_path2}\n请检查文件路径和格式")
                return
        
        # 使用ORB检测关键点和描述符
        orb = cv2.ORB_create()
        keypoints2, descriptors2 = orb.detectAndCompute(img2, None)
        show_image(img2, "Image 2")

# 显示图片
def show_image(image, title):
    cv2.imshow(title, image)
    cv2.waitKey(1)  # 等待1ms，以便更新窗口

# 特征匹配
def match_features():
    global img1, img2, keypoints1, keypoints2, descriptors1, descriptors2
    if img1 is not None and img2 is not None and descriptors1 is not None and descriptors2 is not None:
        # 获取选择的算法
        selected_algorithm = algorithm_var.get()
        
        # 初始化检测器
        brisk = cv2.BRISK_create()
        orb = cv2.ORB_create()
        sift = cv2.SIFT_create()
        akaze = cv2.AKAZE_create()
        
        # 初始化匹配器
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        bf_l2 = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)  # 用于SIFT

        if selected_algorithm == "BRISK":
            # BRISK匹配
            _, descriptors_brisk1 = brisk.compute(img1, keypoints1)
            _, descriptors_brisk2 = brisk.compute(img2, keypoints2)
            matches = bf.match(descriptors_brisk1, descriptors_brisk2)
            img_matches = cv2.drawMatches(img1, keypoints1, img2, keypoints2, matches, None, flags=2)
            window_title = 'BRISK Matches'
        
        elif selected_algorithm == "ORB":
            # ORB匹配
            matches = bf.match(descriptors1, descriptors2)
            img_matches = cv2.drawMatches(img1, keypoints1, img2, keypoints2, matches, None, flags=2)
            window_title = 'ORB Matches'
        
        elif selected_algorithm == "SIFT":
            # SIFT匹配
            keypoints_sift1, descriptors_sift1 = sift.detectAndCompute(img1, None)
            keypoints_sift2, descriptors_sift2 = sift.detectAndCompute(img2, None)
            matches = bf_l2.match(descriptors_sift1, descriptors_sift2)
            img_matches = cv2.drawMatches(img1, keypoints_sift1, img2, keypoints_sift2, matches, None, flags=2)
            window_title = 'SIFT Matches'
        
        elif selected_algorithm == "AKAZE":
            # AKAZE匹配
            keypoints_akaze1, descriptors_akaze1 = akaze.detectAndCompute(img1, None)
            keypoints_akaze2, descriptors_akaze2 = akaze.detectAndCompute(img2, None)
            matches = bf.match(descriptors_akaze1, descriptors_akaze2)
            img_matches = cv2.drawMatches(img1, keypoints_akaze1, img2, keypoints_akaze2, matches, None, flags=2)
            window_title = 'AKAZE Matches'

        # 创建新窗口并显示匹配结果
        cv2.namedWindow(window_title, cv2.WINDOW_NORMAL)
        cv2.imshow(window_title, img_matches)

        # 等待任意键按下，然后关闭所有窗口
        while True:
            key = cv2.waitKey(1) & 0xFF
            if key == 27 or key == ord('q'):  # ESC键或q键退出
                break
        
        cv2.destroyAllWindows()
        # 确保所有窗口都被正确关闭
        for i in range(4):
            cv2.waitKey(1)

# 制作者显示
def show_message():
    label.config(text="一个苦逼的中国大学生，随意转载，LMEater1707制作")

# 创建主窗口
root.title("Sar影像特征匹配系统")

# 创建一个标签，用于显示信息
label = tk.Label(root, text="")
label.pack(pady=20)

# 创建算法选择下拉菜单
algorithm_var = tk.StringVar(root)
algorithm_var.set("BRISK")  # 默认选择
algorithm_menu = tk.OptionMenu(root, algorithm_var, "BRISK", "ORB", "SIFT", "AKAZE")
algorithm_menu.pack(pady=5)

# 创建按钮
button = tk.Button(root, text="制作学生信息", command=show_message)
button.pack(pady=10)

button_select_first = tk.Button(root, text="选择第一个图片", command=select_first_image)
button_select_first.pack(pady=5)

button_select_second = tk.Button(root, text="选择第二个图片", command=select_second_image)
button_select_second.pack(pady=5)

button_match = tk.Button(root, text="开始匹配", command=match_features)
button_match.pack(pady=5)

# 运行Tkinter事件循环
root.mainloop()
