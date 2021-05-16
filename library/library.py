import os
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
import os




def delete_img_head(base64):
    return base64[base64.find(",") + 1:]

