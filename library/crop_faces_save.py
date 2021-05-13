import dlib  # 人脸识别的库 Dlib
import numpy as np  # 数据处理的库 numpy
import cv2  # 图像处理的库 OpenCv
import os
import base64

# Delete old images
def clear_images(path_save):
    imgs = os.listdir(path_save)

    for img in imgs:
        os.remove(path_save + img)

    # print("img clean finish", '\n')


def face_segmentation(img):
    # dlib预测器
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor('../data/dlib/shape_predictor_68_face_landmarks.dat')
    faces = detector(img, 1)

    print("人脸数 / faces in all:", len(faces))
    return faces


def generate_images(faces, img, path_save, single_face=False):
    if single_face:
        a, b = 130, 80
    else:

        if len(faces) > 13:
            a, b = 20, 10
        else:
            a, b = 40, 30

    for num, face in enumerate(faces):

        # 计算矩形大小
        # (x,y), (宽度width, 高度height)
        # print(face)

        # pos_start = tuple([face.left(), face.top()])
        # pos_end = tuple([face.right(), face.bottom()])

        # 计算矩形框大小
        height = face.bottom() - face.top() + a
        width = face.right() - face.left() + a

        # 根据人脸大小生成空的图像
        img_blank = np.zeros((height, width, 3), np.uint8)

        for i in range(height):
            for j in range(width):
                img_blank[i][j] = img[face.top() - b + i][face.left() - b + j]

        # 存在本地
        cv2.imwrite(path_save + str(num + 1) + ".jpg", img_blank)


def face2_local(path_img=None):
    if path_img:
        path_read = path_img
    else:
        # 读取图像的路径
        path_read = "../data/images/cin/204804246.jpg"

    not_boder_img = cv2.imread(path_read)

    # 加边框
    bordersize = 100
    img = cv2.copyMakeBorder(not_boder_img, top=bordersize, bottom=bordersize, left=bordersize,
                             right=bordersize, borderType=cv2.BORDER_CONSTANT)

    # 用来存储生成的单张人脸的路径
    path_save = "../data/images/cout/"
    clear_images(path_save)
    faces = face_segmentation(img)

    # 循环存到cout
    generate_images(faces, img, path_save)


def face2_base64(img_base64, single_face=True):

    # base64转cv2
    imgString = base64.b64decode(img_base64)
    nparr = np.fromstring(imgString, np.uint8)
    not_boder_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # not_boder_img = cv2.imread(path_read)

    # 加边框
    bordersize = 100
    img = cv2.copyMakeBorder(not_boder_img, top=bordersize, bottom=bordersize, left=bordersize,
                             right=bordersize, borderType=cv2.BORDER_CONSTANT)

    # 用来存储生成的单张人脸的路径
    path_save = "../data/images/cout/"
    faces = face_segmentation(img)

    if single_face:
        a, b = 130, 80

    for num, face in enumerate(faces):
        # 计算矩形框大小
        height = face.bottom() - face.top() + a
        width = face.right() - face.left() + a

        # 根据人脸大小生成空的图像
        img_blank = np.zeros((height, width, 3), np.uint8)

        for i in range(height):
            for j in range(width):
                img_blank[i][j] = img[face.top() - b + i][face.left() - b + j]
        if single_face:
            base64_str = cv2.imencode('.jpg', img_blank)[1].tostring()
            base64_str = base64.b64encode(base64_str)
            return base64_str


# face2(path_img=xx,single_face=True)
