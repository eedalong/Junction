# -*- coding: UTF-8 -*-

# 导入系统库并定义辅助函数
import cv2
import time
import base64
from pprint import pformat
from UserEmotion.PythonSDK.facepp import API
import numpy as np
# 导入图片处理类

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
    time_used = result[u'time_used']
    cv2.putText(img, "time_used:{:0f} ms".format(time_used), (0,30), cv2.FONT_HERSHEY_COMPLEX,
                0.7, (0, 0, 255), 1)
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
        # print(face_landmark)
        left_eye = [face_landmark[u'left_eye_left_corner'][u'x'], face_landmark[u'left_eye_top'][u'y'],
                    face_landmark[u'left_eye_right_corner'][u'x'], face_landmark[u'left_eye_bottom'][u'y']]
        right_eye = [face_landmark[u'right_eye_left_corner'][u'x'], face_landmark[u'right_eye_top'][u'y'],
                    face_landmark[u'right_eye_right_corner'][u'x'], face_landmark[u'right_eye_bottom'][u'y']]
        cv2.rectangle(img, (left_eye[0], left_eye[1]), (left_eye[2], left_eye[3]), (255, 0, 0))
        cv2.rectangle(img, (right_eye[0], right_eye[1]), (right_eye[2], right_eye[3]), (255, 0, 0))

        # Draw ethe attributes
        face_attributes = face[u'attributes']
        faceConfidence = face_attributes[u'facequality'][u'value']
        cv2.putText(img, "faceConfidence:{:.1f} ".format(faceConfidence),(x1, y1+20), cv2.FONT_HERSHEY_COMPLEX,
                    0.7, (0, 0, 255), 1)
        face_emotion = face_attributes[u'emotion']
        # print (face_emotion)
        # print (face_emotion.values())
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
        cv2.putText(img, "mouth open:{:.1f} ".format(mouthopenstatus), (x1, y1), cv2.FONT_HERSHEY_COMPLEX,
                    0.7, (0, 0, 255), 1)


class UserEmotion():

    def __init__(self, eye_length = 6):
        self.api = API()
        self.left_eye_size = []
        self.right_eye_size = []
        self.left_max_size = -1
        self.right_max_size = -1
        self.eye_length = eye_length
        self._init_camera()
        # cv2.namedWindow('frame', cv2.WINDOW_NORMAL)

    def _init_camera(self):
        self.cap = cv2.VideoCapture(0)
        #self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640);
        #self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 320);


    def _eye_size_adapt(self, left_eye, right_eye):

        assert len(self.left_eye_size) == len(self.right_eye_size)
        if len(self.left_eye_size) < self.eye_length:
            self.left_eye_size.append(left_eye)
            self.right_eye_size.append(right_eye)
            self.left_max_size = max(self.left_eye_size)
            self.right_max_size = max(self.right_eye_size)
        else:
            self.left_eye_size.pop(0)
            self.left_eye_size.append(left_eye)
            self.right_eye_size.pop(0)
            self.right_eye_size.append(right_eye)

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
            # face_info['bbox'] = [x1, y1, x2, y2]

            # The landmarks
            face_landmark = face[u'landmark']
            left_eye_coor = [face_landmark[u'left_eye_left_corner'][u'x'], face_landmark[u'left_eye_top'][u'y'],
                        face_landmark[u'left_eye_right_corner'][u'x'], face_landmark[u'left_eye_bottom'][u'y']]
            right_eye_coor = [face_landmark[u'right_eye_left_corner'][u'x'], face_landmark[u'right_eye_top'][u'y'],
                         face_landmark[u'right_eye_right_corner'][u'x'], face_landmark[u'right_eye_bottom'][u'y']]
            left_eye = (left_eye_coor[2] - left_eye_coor[0]) * (left_eye_coor[3] - left_eye_coor[1])
            right_eye = (right_eye_coor[2] - right_eye_coor[0]) * (right_eye_coor[3] - right_eye_coor[1])

            self._eye_size_adapt(left_eye, right_eye)
            # print ("Left {}, Max {}\nRight {}, Max {}".format(self.left_eye_size, self.left_max_size,
            #                                           self.right_eye_size, self.right_max_size))
            left_ratio = [(1 - x/float(self.left_max_size)) for x in self.left_eye_size]
            right_ratio = [(1 - x/float(self.right_max_size)) for x in self.right_eye_size]
            ratio = left_ratio + right_ratio
            eye_ratio = sum(ratio)/len(ratio)
            # print ("Left Ratio {}\nRight Ratio {}\nEye Ratio :{}".format(left_ratio, right_ratio, eye_ratio))
            face_info['tired'] = eye_ratio
            # The attributes
            face_attributes = face[u'attributes']

            # The emotion
            face_emotion = face_attributes[u'emotion']
            # emotion : ['neutral', 'disgust', 'anger', 'surprise', 'fear', 'sadness', 'happiness']
            face_info['emotion'] = face_emotion.values()

            # The quality
            faceConfidence = face_attributes[u'facequality'][u'value']
            face_info['faceConfidence'] = faceConfidence

            result_post.append(face_info)

        if len(result_post) == 0:
            result_post = None
        else:
            result_post = result_post[0]
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

    def getData(self, siteID=None, sensorID=None, startTimeStamp=None, endTimeStamp=None):
        return self.detect()

    def detect(self):
        # Convert the array image to base64
        frame = None
        sample = np.ndarray((4,5))
        while not isinstance(frame,type(sample)):
            ret, frame = self.cap.read()

        retval, buffer = cv2.imencode('.jpg', frame)
        frame_base64 = base64.b64encode(buffer)
        tic = time.time()
        res = self.api.detect(image_base64=frame_base64, return_landmark=2,
                              return_attributes="gender,age,smiling,headpose,facequality,"
                                                "blur,eyestatus,emotion,ethnicity,beauty,"
                                                "mouthstatus,skinstatus")
        print('Consume {:0f} s'.format(time.time() - tic))
        result = self._result_postprocessing(res)
        self._draw_result(frame, res)
        cv2.imshow('frame', frame)
        cv2.waitKey()
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
        print('Sending image...')
        tic = time.time()
        res = api.detect(image_base64=frame_base64, return_landmark=2,
                         return_attributes="gender,age,smiling,headpose,facequality,"
                                           "blur,eyestatus,emotion,ethnicity,beauty,"
                                           "mouthstatus,skinstatus")
        # print('Consume {:0f} ms'.format(time.time() - tic))
        draw_result(frame, res)
        print('Consume {:0f} s'.format(time.time() - tic))
        # Display the resulting frame
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

