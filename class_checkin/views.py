from library.library import *
from library.crop_faces_save import *

######################################### init
ip = "10.6.0.39"  # 设置度目ip
BASE_DIR = Path(__file__).resolve().parent.parent
# 所有学生
room = "$"
students = {}
students_isroom = {}
students_notroom = {}


######################################## init end

def message(request):
    if request.method == 'POST':
        jsonStr = request.body.decode()
        jsonDate = json.loads(jsonStr)

        if jsonDate.get("state", "-1") == 'class_checkin':
            imageData = jsonDate.get("imageData", "")
            if imageData:
                img1 = delete_img_head(imageData)
                pic_faces = face2_base64_recognize(img1)
                class_checkin(pic_faces) #图片全部人脸数组传入
                return JsonResponse({'state': '1', 'log': "包含图片"})
            else:
                return JsonResponse({'state': '-1', 'log': "未上传图片数据"})
        if jsonDate.get("state", "-1") == 'register_face':
            imageData = jsonDate.get("imageData", "")
            studentId = jsonDate.get("studentId", "")
            if imageData and studentId[::-1][:1] == 'x' or studentId[::-1][:1] == 'X':
                # 去除x
                studentId = studentId[0:len(studentId) - 1]
                img1 = face2_base64(delete_img_head(imageData))
                res = addDUMUface(imageData=img1, studentId=studentId, head=False)
                return JsonResponse(res)
            else:
                return JsonResponse({'state': '-1', 'log': "请求数据不正确"})
            pass



        else:
            return HttpResponse("clockin")


# 向度目发送数据  返回值为ssid   默认head=True加base64加头文本
def sendDUMU(imageData, head=True):
    global ip

    url = "http://" + ip + ":8080/recognitionManage/identify"
    if head:
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

# 向度目添加人脸数据
def addDUMUface(imageData, studentId, head=True):
    global ip

    # 注册用户接口
    url = "http://" + ip + ":8080/userManage/addUser"

    if head:
        imageData = imageData[imageData.find(",") + 1:]

    data = {
        "pass": "1a100d2c0dab19c4430e7d73762b3423",
        "user_id": studentId,
        "image_content": imageData,
        "image_type": "image",
        "user_info": {"name": studentId, "phone_number": "1234567891"},
        "action_type": "APPEND",
        "quality_control": "NONE",
        "auth_start_time": 0,
        "auth_end_time": 0
    }

    headers = {'Content-Type': 'application/json'}

    res = req.post(url=url, headers=headers, data=json.dumps(data)).json()

    if res.get("code", True):
        print("注册人脸成功", studentId)
        return {"state": "1", "log": "成功"}
    else:
        print("注册人脸失败", studentId)
        return {"state": "-1", "log": res.get("log")}

def class_checkin(pic_faces):
    # 此处需要 一个图片人脸数组
    students_id = []
    for pic in pic_faces:
        students_id.append(sendDUMU(imageData=pic, head=False))
    print(students_id)