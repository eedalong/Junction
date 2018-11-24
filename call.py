# -*- coding: UTF-8 -*-

# 导入系统库并定义辅助函数
import cv2
import base64
from pprint import pformat
from PythonSDK.facepp import API,File

# 导入图片处理类
import PythonSDK.ImagePro

# 以下四项是dmeo中用到的图片资源，可根据需要替换
detech_img_url = 'http://bj-mc-prod-asset.oss-cn-beijing.aliyuncs.com/mc-official/images/face/demo-pic11.jpg'
faceSet_img = './imgResource/demo.jpeg'       # 用于创建faceSet
face_search_img = './imgResource/search.png'  # 用于人脸搜索
segment_img = './imgResource/segment.jpg'     # 用于人体抠像
merge_img = './imgResource/merge.jpg'         # 用于人脸融合


# 此方法专用来打印api返回的信息
def print_result(hit, result):
    print(hit)
    print('\n'.join("  " + i for i in pformat(result, width=75).split('\n')))

def printFuctionTitle(title):
    return "\n"+"-"*60+title+"-"*60;

def draw_result(img, result):
    faces = result[u'faces']
    for i in range(len(faces)):
        face = faces[i]
        # Draw the bounding box
        face_rectangle = face[u'face_rectangle']
        x1 = face_rectangle[u'left']
        y1 = face_rectangle[u'top']
        x2 = x1 + face_rectangle[u'width']
        y2 = y1 + face_rectangle[u'height']
        cv2.rectangle(img, (x1,y1), (x2,y2), (255, 0, 0))
        # Draw the landmarks
        face_landmark = face[u'landmark']

        # Draw the attributes
        face_attributes = face[u'attributes']
        face_emotion = face_attributes[u'emotion']
        print (face_emotion)
        print (face_emotion.values())
        emotion = max(face_emotion, key=face_emotion.get)
        emotion_score = face_emotion[emotion]
        cv2.putText(img,"{}:{:.1f}".format(emotion, emotion_score), (x1,y1-40), cv2.FONT_HERSHEY_COMPLEX,
                    0.7, (0,0,255), 1)
        face_headpose = face_attributes[u'headpose']
        pitch_angle = face_headpose[u'pitch_angle']
        roll_angle = face_headpose[u'roll_angle']
        yaw_angle = face_headpose[u'yaw_angle']
        cv2.putText(img, "yaw:{:.0f} roll:{:.0f} pitch:{:.0f}".format(yaw_angle, roll_angle, pitch_angle),
                    (x1, y1-20), cv2.FONT_HERSHEY_COMPLEX,0.7, (0, 0, 255), 1)
        face_mouthstatus = face_attributes[u'mouthstatus']
        mouthopenstatus = face_mouthstatus[u'open']
        cv2.putText(img, "mouth open:{:.1f} ".format(mouthopenstatus,),(x1, y1), cv2.FONT_HERSHEY_COMPLEX,
                    0.7, (0, 0, 255), 1)



class FaceDetector():

    def __init__(self):
        self.api = API()
        self._init_camera()

    def _init_camera(self):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640);
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 320);

    def _result_postprocessing(self, result):
        result_post = []
        faces = result[u'faces']
        for i in range(len(faces)):
            face = faces[i]
            face_info = {}
            # The bounding box
            face_rectangle = face[u'face_rectangle']
            x1 = face_rectangle[u'left']
            y1 = face_rectangle[u'top']
            x2 = x1 + face_rectangle[u'width']
            y2 = y1 + face_rectangle[u'height']
            # bbox : [x1, y1, x2, y2]
            face_info['bbox'] = [x1, y1, x2, y2]

            # The landmarks
            face_landmark = face[u'landmark']
            # face_info['landmark'] = face_landmark

            # The attributes
            face_attributes = face[u'attributes']

            # The emotion
            face_emotion = face_attributes[u'emotion']
            # emotion : ['neutral', 'disgust', 'anger', 'surprise', 'fear', 'sadness', 'happiness']
            face_info['emotion'] = face_emotion.values()

            # The headpose
            face_headpose = face_attributes[u'headpose']
            pitch_angle = face_headpose[u'pitch_angle']
            roll_angle = face_headpose[u'roll_angle']
            yaw_angle = face_headpose[u'yaw_angle']
            # headpose : [pitch_angle, roll_angle, yaw_angle]
            face_info['headpose'] = [pitch_angle, roll_angle, yaw_angle]
            face_mouthstatus = face_attributes[u'mouthstatus']
            mouthopenstatus = face_mouthstatus[u'open']

            result_post.append(face_info)

        return result_post

    def _draw_result(self, img, result):
        faces = result[u'faces']
        for i in range(len(faces)):
            face = faces[i]
            # Draw the bounding box
            face_rectangle = face[u'face_rectangle']
            x1 = face_rectangle[u'left']
            y1 = face_rectangle[u'top']
            x2 = x1 + face_rectangle[u'width']
            y2 = y1 + face_rectangle[u'height']
            cv2.rectangle(img, (x1,y1), (x2,y2), (255, 0, 0))
            # Draw the landmarks
            face_landmark = face[u'landmark']

            # Draw the attributes
            face_attributes = face[u'attributes']
            face_emotion = face_attributes[u'emotion']
            print (face_emotion)
            print (face_emotion.values())
            emotion = max(face_emotion, key=face_emotion.get)
            emotion_score = face_emotion[emotion]
            cv2.putText(img,"{}:{:.1f}".format(emotion, emotion_score), (x1,y1-40), cv2.FONT_HERSHEY_COMPLEX,
                        0.7, (0,0,255), 1)
            face_headpose = face_attributes[u'headpose']
            pitch_angle = face_headpose[u'pitch_angle']
            roll_angle = face_headpose[u'roll_angle']
            yaw_angle = face_headpose[u'yaw_angle']
            cv2.putText(img, "yaw:{:.0f} roll:{:.0f} pitch:{:.0f}".format(yaw_angle, roll_angle, pitch_angle),
                        (x1, y1-20), cv2.FONT_HERSHEY_COMPLEX,0.7, (0, 0, 255), 1)
            face_mouthstatus = face_attributes[u'mouthstatus']
            mouthopenstatus = face_mouthstatus[u'open']
            cv2.putText(img, "mouth open:{:.1f} ".format(mouthopenstatus,),(x1, y1), cv2.FONT_HERSHEY_COMPLEX,
                        0.7, (0, 0, 255), 1)


    def detect(self):
        # Convert the array image to base64
        ret, frame = self.cap.read()
        retval, buffer = cv2.imencode('.jpg', frame)
        frame_base64 = base64.b64encode(buffer)
        res = self.api.detect(image_base64=frame_base64, return_landmark=2,
                              return_attributes="gender,age,smiling,headpose,facequality,"
                                                "blur,eyestatus,emotion,ethnicity,beauty,"
                                                "mouthstatus,skinstatus")

        result = self._result_postprocessing(res)
        # self._draw_result(frame, res)
        # cv2.imshow('frame', frame)
        # cv2.waitKey(0)
        return result

    def close(self):
        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    # 初始化对象，进行api的调用工作
    api = API()
    # -----------------------------------------------------------人脸识别部分-------------------------------------------

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640);
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 320);

    while (True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        cnt = cv2.imencode('.png', frame)[1]
        retval, buffer = cv2.imencode('.jpg', frame)
        frame_base64 = base64.b64encode(buffer)
        # frame_base64 = base64.b64encode(frame)
        res = api.detect(image_base64=frame_base64, return_landmark=2,
                         return_attributes="gender,age,smiling,headpose,facequality,"
                                           "blur,eyestatus,emotion,ethnicity,beauty,"
                                           "mouthstatus,skinstatus")
        draw_result(frame, res)

        # Display the resulting frame
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

# ----------------------------------------------------------人脸识别部分(单张图片)-----------------------------------------

# img = cv2.imread(segment_img)
# with open(segment_img, "rb") as f:
#     data = f.read()
#     img_base64 = data.encode("base64")
#
# # 人脸检测：https://console.faceplusplus.com.cn/documents/4888373
# res = api.detect(image_base64=img_base64, return_landmark=2,
#                  return_attributes="gender,age,smiling,headpose,facequality,"
#                                                        "blur,eyestatus,emotion,ethnicity,beauty,"
#                                                        "mouthstatus,skinstatus")
# print_result(printFuctionTitle("人脸检测"), res)
# draw_result(img, res)
# cv2.imshow("a", img)
# cv2.waitKey(0)

# 人脸比对：https://console.faceplusplus.com.cn/documents/4887586
# compare_res = api.compare(image_file1=File(face_search_img), image_file2=File(face_search_img))
# print_result("compare", compare_res)

# 人脸搜索：https://console.faceplusplus.com.cn/documents/4888381
# 人脸搜索步骤
# 1,创建faceSet:用于存储人脸信息(face_token)
# 2,向faceSet中添加人脸信息(face_token)
# 3，开始搜索

# 删除无用的人脸库，这里删除了，如果在项目中请注意是否要删除
# api.faceset.delete(outer_id='faceplusplus', check_empty=0)
# # 1.创建一个faceSet
# ret = api.faceset.create(outer_id='faceplusplus')
#
# # 2.向faceSet中添加人脸信息(face_token)
# faceResStr=""
# res = api.detect(image_file=File(faceSet_img))
# faceList = res["faces"]
# for index in range(len(faceList)):
#     if(index==0):
#         faceResStr = faceResStr + faceList[index]["face_token"]
#     else:
#         faceResStr = faceResStr + ","+faceList[index]["face_token"]
#
# api.faceset.addface(outer_id='faceplusplus', face_tokens=faceResStr)
#
# # 3.开始搜索相似脸人脸信息
# search_result = api.search(image_file=File(face_search_img), outer_id='faceplusplus')
# print_result('search', search_result)

# -----------------------------------------------------------人体识别部分-------------------------------------------

# 人体抠像:https://console.faceplusplus.com.cn/documents/10071567
# segment_res = api.segment(image_file=File(segment_img))
# f = open('./imgResource/demo-segment.b64', 'w')
# f.write(segment_res["result"])
# f.close()
# print_result("segment", segment_res)
# # 开始抠像
#
# PythonSDK.ImagePro.ImageProCls.getSegmentImg("./imgResource/demo-segment.b64")

# -----------------------------------------------------------证件识别部分-------------------------------------------
# 身份证识别:https://console.faceplusplus.com.cn/documents/5671702
# ocrIDCard_res = api.ocridcard(image_url="https://gss0.bdstatic.com/94o3dSag_xI4khGkpoWK1HF6hhy/baike/"
#                                         "c0%3Dbaike80%2C5%2C5%2C80%2C26/sign=7a16a1be19178a82da3177f2976a18e8"
#                                         "/902397dda144ad34a1b2dcf5d7a20cf431ad85b7.jpg")
# print_result('ocrIDCard', ocrIDCard_res)

# 银行卡识别:https://console.faceplusplus.com.cn/documents/10069553
# ocrBankCard_res = api.ocrbankcard(image_url="http://pic.5tu.cn/uploads/allimg/1107/191634534200.jpg")
# print_result('ocrBankCard', ocrBankCard_res)

# -----------------------------------------------------------图像识别部分-------------------------------------------
# 人脸融合：https://console.faceplusplus.com.cn/documents/20813963
# template_rectangle参数中的数据要通过人脸检测api来获取
# mergeFace_res = api.mergeface(template_file=File(segment_img), merge_file=File(merge_img),
#                               template_rectangle="130,180,172,172")
# print_result("mergeFace", mergeFace_res)
#
# # 开始融合
# PythonSDK.ImagePro.ImageProCls.getMergeImg(mergeFace_res["result"])
