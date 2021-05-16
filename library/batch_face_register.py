import os
import base64
import time

import requests
import json

###################################
"""
用于批量注册人脸
F:\ls
格式 204804246.jpg



"""


###############################


def batch_face_register(ls):
    dir = os.path.join(ls)

    for root, dirs, files in os.walk(dir):
        for name in files:
            dizhi = os.path.join(root, name)
            if dizhi[-5] == ')':
                continue
            print(dizhi, dizhi[6:15])

            with open(dizhi, "rb") as pic:
                pic_base64 = base64.b64encode(pic.read()).decode()

            data = {
                "state": "register_face",
                "studentId": dizhi[6:15] + "x",
                "imageData": pic_base64
            }
            data = json.dumps(data)
            # print(data)
            res = requests.post('http://127.0.0.1:8000/class_clockin/', data=data).json()
            print(res)
            time.sleep(10)
            # break

    pass

def batch_face_register02(ls):
    dir = os.path.join(ls)

    for root, dirs, files in os.walk(dir):
        for name in files:
            dizhi = os.path.join(root, name)
            if dizhi[-5] == ')':

                print(dizhi, dizhi[6:15])

                with open(dizhi, "rb") as pic:
                    pic_base64 = base64.b64encode(pic.read()).decode()

                data = {
                    "state": "register_face",
                    "studentId": dizhi[6:15] + "x",
                    "imageData": pic_base64
                }
                data = json.dumps(data)
                # print(data)
                res = requests.post('http://127.0.0.1:8000/class_clockin/', data=data).json()
                print(res)
                time.sleep(10)
                # break

    pass


batch_face_register02("F:\ls")
