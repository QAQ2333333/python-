import requests
from pydub import AudioSegment
from pydub.playback import play
from http import HTTPStatus
import dashscope
import pygame
import time
import speech_recognition as sr

dashscope.api_key = ""


def speech():

    try:
        recognizer = sr.Recognizer()

        with sr.Microphone() as source:
            print("请开始说话...")

            recognizer.adjust_for_ambient_noise(source)

            print(1)
            audio = recognizer.listen(source,timeout=5)
            print(2)

        print("正在识别...")
        text = recognizer.recognize_google(audio, language='zh-CN')

        if '你好' in text:
            print(text)
            return text
        else:
            print(text)
            return 1

    except:
        print('未识别')
        return 1



def ask(question):
    response = (dashscope.Generation.call
    (
        model='qwen-plus',
        prompt=f'（回答必须在100字以内！可能会有错别字）以下是问题：{question}'
    ))

    re = response.output
    get = re['text']
    print(get)

    return get


def tts(texts):
    url = "https://bv2.firefly.matce.cn/run/predict"
    data = {
        "data": [
            f'{texts}',
            "流萤_ZH",
            0.5,
            0.6,
            0.9,
            1,
            "ZH",
            True,
            1,
            0.2,
            None,
            "Happy",
            "",
            0.7
        ],
        "event_data": None,
        "fn_index": 0,
        "session_hash": "n77b1q5fjns"
    }

    headers = {
        "Content-Type": "application/json",
    }

    response = requests.post(url, json=data, headers=headers)
    print(response)
    re = response.json()
    print(re)
    getwav = re['data'][1]['name']
    geturl = 'https://bv2.firefly.matce.cn/file=' + getwav

    rewav = requests.get(geturl).content

    with open(r"C:\Users\苏\Desktop\py\music\musics.wav", 'wb') as f:
        f.write(rewav)
        print('完成')


def playmu():
    pygame.init()

    pygame.mixer.music.load(r"C:\Users\苏\Desktop\py\music\musics.wav")
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        time.sleep(1)

    pygame.quit()


def main():
    while True:
        a = speech()

        if a == 1:
            continue

        else:

            answer = ask(a)
            tts(answer)
            playmu()


if __name__ == '__main__':
    main()



