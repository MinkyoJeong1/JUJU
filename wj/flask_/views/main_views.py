from flask import Blueprint, render_template, request, url_for
from werkzeug.utils import redirect

# import os
# print(os.getcwd())

'''
import sys
import os
wav_lib = "Wav2Lip"
absolute_path = os.path.abspath(wav_lib)
sys.path.append(absolute_path)

print("000===", absolute_path)
print("001===",sys.path)
'''

from Wav2Lip import inference as Inf
import os

import time
import threading

from enum import Enum, auto

py_path = "Wav2Lip/inference.py"
model_path = "Wav2Lip/checkpoints/wav2lip_gan.pth"

bp = Blueprint('main', __name__,url_prefix='/' )

#inf = Inf()
# TODO _ 로드 한번 되었으면 또 로드되지 않도록 처리
Inf.load_model(model_path)

# 추론 결과를 저장할 변수
inf_completed = False

class E_emo(Enum):
    fear = auto()  # 1
    angry = auto()
    disgust = auto()
    happiness = auto()
    neutral = auto()
    sadness = auto()
    surprise = auto()

# 스레드 1 :  추론
def thd_inference(cmd, face_p, audio_p):
    print("Inffffff")
    #os.system(cmd)
    Inf.addparser(model_path,face_p,audio_p)
    Inf.main()
    
    time.sleep(5)

# 스레드 2 :  결과 파일 생성 확인
def thd_new_files():
    global inf_completed
    target_folder = "Wav2Lip/results"  # D:/GitHub/JUJUbot/wj/ 감시할 폴더 경로

    while True:
        time.sleep(1)  # 1초마다 폴더 스캔
        files = os.listdir(target_folder)
        new_files = [file for file in files if file.endswith(".mp4")]  # 새로운 .txt 파일 찾기

        if new_files:
            inf_completed = True
            print("새로운 파일이 생성되었습니다:", new_files)


@bp.route('/inf')
def start_infer(file_p, audio_p):
    # 추론
        #   테스트용 파일
        print(os.getcwd()) #D:\GitHub\JUJUbot\wj
        root = os.getcwd()
        face_path = os.path.join(root, "flask_", "static", "video", "01.mp4")
        audio_path = os.path.join(root, "flask_", "static", "audio", "wav00.wav")
        cmd = 'python ' + py_path + " --checkpoint_path " + model_path + " --face " + face_path + " --audio " + audio_path
        #   추론을 백그라운드에서 실행하는 스레드 생성
        inf_thread = threading.Thread(target=thd_inference, args=(cmd, face_path, audio_path))
        inf_thread.start()

        #   파일 감시를 백그라운드에서 실행하는 스레드 생성
        file_thread = threading.Thread(target=thd_new_files)
        file_thread.start()


@bp.route('/', methods=['GET','POST'])
def main_index():

    if request.method == 'POST':
        print(request.files)

        # 보이스 데이터 받기
        #voice = request.files['voice']
        # 감정 분류 데이터 받기
        #emo = request.files['emo']
        # 감정에 따른 기본 영상 선택

        
        # 추론
        #   테스트용 파일
        print(os.getcwd()) #D:\GitHub\JUJUbot\wj
        root = os.getcwd()
        face_path = os.path.join(root, "flask_", "static", "video", "01.mp4")#root + r"flask_\static\video\01.mp4"
        audio_path = os.path.join(root, "flask_", "static", "audio", "wav00.wav")#root + r"flask_\static\audio\wav00.wav"
        cmd = 'python ' + py_path + " --checkpoint_path " + model_path + " --face " + face_path + " --audio " + audio_path
        #   추론을 백그라운드에서 실행하는 스레드 생성
        inf_thread = threading.Thread(target=thd_inference, args=(cmd, face_path, audio_path))
        inf_thread.start()

        #   파일 감시를 백그라운드에서 실행하는 스레드 생성
        file_thread = threading.Thread(target=thd_new_files)
        file_thread.start()
        
        return render_template("base.html", inf_completed=inf_completed)
    
    return render_template("base.html", inf_completed=inf_completed)