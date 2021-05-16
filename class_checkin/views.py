from library.library import *
from library.crop_faces_save import *
from class_checkin.models import class_student, query_log

######################################### init
ip = "10.6.0.39"  # 设置度目ip3
BASE_DIR = Path(__file__).resolve().parent.parent
# 所有学生
room = "$"


# students = {}
# students_isroom = {}
# students_notroom = {}


######################################## init end

def message(request):
    if request.method == 'POST':
        jsonStr = request.body.decode()
        jsonDate = json.loads(jsonStr)

        if jsonDate.get("state", "-1") == 'class_checkin':
            imageData = jsonDate.get("imageData", "")
            continueValidate = jsonDate.get("continueValidate", "0")
            if imageData:
                img1 = delete_img_head(imageData)
                pic_faces = face2_base64_recognize(img1)
                result = class_checkin(pic_faces, continueValidate)  # 图片全部人脸数组传入
                return JsonResponse(result, safe=False)
            else:
                return JsonResponse({'state': '-1', 'log': "未上传图片数据"})
        if jsonDate.get("state", "-1") == 'register_face':
            """
            {
                "state":"register_face",
                "studentId":"204804246x",
                "imageData":"data:image/jpeg;base64,/9j/"
            }
            """
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


# 批量班级考勤
def class_checkin(pic_faces, Continue_validate=False):
    global room
    room = ''
    # 此处需要 一个图片人脸数组
    students_id = set()
    hq_class = dict()
    for pic in pic_faces:
        students_id.add(sendDUMU(imageData=pic, head=False))

    # print(students_id)

    ########################
    # 更新room
    k = 0
    for l in students_id:
        k += 1
        if k > 5:  # 循环5次
            break

        stds = class_student.objects.filter(sid__exact=l)
        if len(stds) >= 1:
            std = stds[0].class_room

            if hq_class.get(std):
                hq_class[std] = hq_class[std] + 1
            else:
                hq_class[std] = 1

    hq_class2 = list()
    for b in hq_class.values():
        hq_class2.append(b)
    hq_class2.sort()
    for a, b in hq_class.items():
        if b == hq_class2[len(hq_class2) - 1]:
            room = a

    if room == '':
        return {'state': '-1', 'log': "未获取到班级"}
    ########################

    stu_all = class_student.objects.filter(class_room__exact=room)
    if Continue_validate == False:
        stu_all.update(isroom=False)

    print(students_id)
    for id in students_id:
        stds = stu_all.all().filter(sid__exact=id)
        if len(stds):
            stds.update(isroom=True)

    # notroom = stu_all.all().filter(isroom__exact=False)
    # isroom = stu_all.all().filter(isroom__exact=True)
    students = list()
    students.clear()
    """
        [{id:'',name:'',isroom:''},
        ]
    """

    for i in stu_all.all():
        tmp = {'sid': i.sid, 'name': i.name, 'isroom': i.isroom}
        students.append(tmp)

    add_query_log(students)
    return students


def add_query_log(log):
    global room
    log = str([log])
    date = datetime.datetime.now()

    data = query_log(class_room=room, date=date, log=log)
    data.save()
