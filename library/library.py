import os
from library.crop_faces_save import face2_local
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
import requests as req

import json
import base64
from pathlib import Path
from library.pic_add_border import image_border
import time
import datetime

# 多线程
import _thread
import threading
import time





def delete_img_head(base64):
    return base64[base64.find(",") + 1:]

