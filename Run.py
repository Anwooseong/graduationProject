import os
import shutil
import psutil
import time
import webbrowser

from RunData import checkDir, makeDir, getSrcPath, getDstPath, getControlDataNames
from LoadingGUI import EncryptLoadingClass, DecryptLoadingClass


def initCheck():
    if not(checkDir()):
        makeDir()


def run(beginTimer, flag, nickname):
    check = 0
    srcPath = getSrcPath()
    dstPath = getDstPath()

    for proc in psutil.process_iter():    # 실행중인 프로세스를 순차적으로 검색
        ps_name = proc.name()               # 프로세스 이름을 ps_name에 할당

        if ps_name == "chrome.exe":
            check = 1

    if(check == 1 and flag == 0):
        # 파일 옮기기
        fileMove(dstPath, srcPath, nickname)

        beginTimer = time.time()

        return beginTimer, 0
    elif(check == 1 and flag == 1):
        os.system('taskkill /f /im chrome.exe')

        decryptclass = DecryptLoadingClass(dstPath, nickname)
        decryptclass.exec()
        print("decrypt done!")

        # 파일 옮기기
        fileMove(dstPath, srcPath, nickname)

        webbrowser.open("https://google.com")
        beginTimer = time.time()

        return beginTimer, 0
    elif (check == 0 and flag == 0):
        # 파일 옮기기
        fileMove(srcPath, dstPath, nickname)

        afterTimer = time.time()

        if((int)(afterTimer - beginTimer) >= 1):   # 타이머 설정
            encryptclass = EncryptLoadingClass(dstPath, nickname)

            encryptclass.exec()
            print("encrypt done!")

            return beginTimer, 1
        else:
            return beginTimer, 0
    elif (check==0 and flag == 1):
        return beginTimer, 1


def fileMove(srcPath, dstPath, nickname):
    filenames = getControlDataNames(nickname)

    for filename in filenames:
        if(os.path.isfile(srcPath + filename)):
            if(os.path.exists(dstPath + filename)):
                os.remove(dstPath + filename)
            shutil.move(srcPath + filename, dstPath + filename)

        elif(os.path.isdir(srcPath + filename)):
            if(os.path.exists(dstPath + filename)):
                shutil.rmtree(dstPath + filename)
            shutil.move(srcPath + filename, dstPath + filename)
