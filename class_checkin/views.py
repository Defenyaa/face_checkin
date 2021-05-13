from library.library import *
from library.crop_faces_save import face2_local, face2_base64
######################################### init
ip = "10.6.0.39"  # 设置度目ip
BASE_DIR = Path(__file__).resolve().parent.parent
room = "$"

# 所有学生
students = {'班级': '班级'}
# 存储在场学生,不在场学生
students_isroom = {}
students_notroom = {}

######################################## init end

def message(request):
    if request.method == 'POST':
        jsonStr = request.body.decode()
        jsonDate = json.loads(jsonStr)

        if jsonDate.get("state", "-1") == 'class_clockin':
            imageData = jsonDate.get("imageData", "")
            if imageData:
                # jsonresponse = faceSegmentation(imageData)
                return JsonResponse({'state': '1', 'log': "包含图片"})
            else:
                return JsonResponse({'state': '-1', 'log': "未上传图片数据"})
        if jsonDate.get("state", "-1") == 'register_face':
            imageData = jsonDate.get("imageData", "")
            if imageData:
                face2_base64(imageData)

                return JsonResponse({'state': '1', 'log': "包含图片"})
            else:
                return JsonResponse({'state': '-1', 'log': "未上传图片数据"})
            pass

        else:
            return HttpResponse("clockin")


# 向度目发送数据
def sendDUMU(imageData):
    global ip

    url = "http://" + ip + ":8080/recognitionManage/identify"

    # 删除imageData前面的头文件 data:image/jpeg;base64,
    imageData = delete_img_head(imageData)

    # 处理data数据
    data = {
        "pass": "1a100d2c0dab19c4430e7d73762b3423",
        "image_content": imageData,
        "image_type": "image",
        "quality_control": "NONE",
        "threshold": 80,
        "user_num": 1
    }

    headers = {'Content-Type': 'application/json'}

    # 转化response为json 字典类型
    res = req.post(url=url, headers=headers, data=json.dumps(data)).json()
    time.sleep(0.1)
    # print("######", res)

    """
    { 
    "user_list":[ { "user_id": "user_id", "user_info": { "name":"name", "phone_number":"12345" },"score": 80 }],
    "code": true,
    "log": "'identify' success!" }
    """

    if res.get("code", True):
        if len(res.get("user_list")):
            ssid = res.get("user_list")[0].get("user_id")

            print("度目:识别id成功----" + ssid)
            return ssid

        else:
            print("度目:无这个人")
            return "2"

    else:
        return "1"

