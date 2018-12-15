import cv2
import numpy as np
import math
import csv

#定義
ESC_KEY = 27
INTERVAL = 33
FRAME_RATE = 30

ORG_WINDOW_NAME = "org"
CALC_WINDOW_NAME = "calculation"

ORG_FILE_NAME = './movie/slow_800hpa.mp4'
CALC_FILE_NAME = './movie/slow_800hpa_calc.mp4'

#色の閾値の設定を行う--------------------------
#赤の閾値
lower_red = np.array([0, 90, 30])
upper_red = np.array([5, 255, 255])
#緑の閾値
lower_green = np.array([50, 50, 50])
upper_green = np.array([80, 255, 255])
#ピンクの閾値
lower_pink = np.array([150, 50, 50])
upper_pink = np.array([170, 255, 255])
#--------------------------------------------

#csvデータの設定
DATA_CSV = './data/data_slow_FHD.csv'
data_dir = './data/'
f = open(DATA_CSV, 'w')

#CSVファイルに書き込むコード
def save_data(past_seconds, bending_deg):
    writer = csv.writer(f)
    writer.writerow([past_seconds, bending_deg])
    return

#ビデオファイルの読み込み
cap = cv2.VideoCapture(ORG_FILE_NAME)
#ビデオファイルのfpsを求める(スマホはfps30)
fps = cap.get(cv2.CAP_PROP_FPS)
print(fps)
count = 0

end_flag, frame = cap.read()
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
#縮小する場合
#size = (640, 480)
rec = cv2.VideoWriter(CALC_FILE_NAME, cv2.VideoWriter_fourcc(*'XVID'), FRAME_RATE, (int(width), int(height)))
cv2.namedWindow(ORG_WINDOW_NAME)
cv2.namedWindow(CALC_WINDOW_NAME)

while end_flag == True:
    #処理を軽くするために動画サイズを縮小する場合。
    #frame = cv2.resize(frame, size)

    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #指定色に基づいてマスク画像の生成
    red_mask = cv2.inRange(frame_hsv, lower_red, upper_red)
    green_mask = cv2.inRange(frame_hsv, lower_green, upper_green)
    pink_mask = cv2.inRange(frame_hsv, lower_pink, upper_pink)

    circles_red = cv2.HoughCircles(red_mask, cv2.HOUGH_GRADIENT,
                                dp=2, minDist=10, param1=25, param2=15,
                                minRadius=10, maxRadius=15)

    circles_green = cv2.HoughCircles(green_mask, cv2.HOUGH_GRADIENT,
                                dp=2, minDist=10, param1=20, param2=10,
                                minRadius=10, maxRadius=15)

    circles_pink = cv2.HoughCircles(pink_mask, cv2.HOUGH_GRADIENT,
                                     dp=2, minDist=10, param1=20, param2=10,
                                     minRadius=10, maxRadius=15)


    # 赤のマーカー
    if circles_red is  not None:
        if(circles_red.shape[1] == 2): #赤色のマーカーが2点検出されている時を計測する。
            x1_root = circles_red[0][0][0]
            y1_root = circles_red[0][0][1]

            x2_root = circles_red[0][1][0]
            y2_root = circles_red[0][1][1]
        else:#その他は前回の値を継承
            x1_root = x1_root
            y1_root = y1_root

            x2_root = x2_root
            y2_root = y2_root

    if circles_green is not None: #まず緑のマーカーが検出されるかどうか。
        if(circles_green.shape[1] == 1):#円検出の数が1つだけである時
        #if (circles_green[0][0][0] != 0): #x座標が0のことがあったのでそれは無視する。
            x1_tip = circles_green[0][0][0]
            y1_tip = circles_green[0][0][1]
        else:
            x1_tip = x1_tip
            y1_tip = y1_tip


    if circles_pink is not None: #ピンクのマーカーが検出されるかどうか。
        if(circles_pink.shape[1] == 1):#円検出の数が1つだけである時
        #if (circles_pink[0][0][0] != 0): #x座標が0のことがあったのでそれは無視する。
            x2_tip = circles_pink[0][0][0]
            y2_tip = circles_pink[0][0][1]
        else:
            x2_tip = x2_tip
            y2_tip = y2_tip

    #根元(赤色の2つのマーカー)のベクトルを求める。
    if(x2_root >= x1_root):
        vec_root = np.array([x2_root- x1_root, y2_root - y1_root])
    else:
        vec_root = np.array([x1_root - x2_root, y1_root - y2_root])

    #先端のベクトルを求める。
    vec_tip = np.array([x2_tip - x1_tip, y2_tip - y1_tip])

    try:
        theta = math.acos(np.dot(vec_root, vec_tip)/ (math.sqrt(np.dot(vec_root, vec_root)) * math.sqrt(np.dot(vec_tip, vec_tip)))) *180 / math.pi
    except:
        print("thetaの値を求める過程でエラー発生")

    print("-----------------")
    print("red1:", x1_root, y1_root)
    print("red2:", x2_root, y2_root)
    print("green", x1_tip, x2_tip)
    print("pink", x2_tip, y2_tip)
    print("-----------------")
    print("vec_root", vec_root)
    print("vec_tip", vec_tip)
    print("theta", theta)

    #描写コード---------------------------------------
    #ハフ変換で検出された円の描写
    try:
        for (x, y, r) in circles_red[0]:
            cv2.circle(frame, (x, y), r, (0, 255, 0), 2)
            cv2.circle(frame, (x, y), 2, (0, 0, 255), 3)
    except:
        pass

    try:
        for (x, y, r) in circles_green[0]:
            cv2.circle(frame, (x, y), r, (0, 255, 0), 2)
            cv2.circle(frame, (x, y), 2, (0, 255, 0), 3)
    except:
        pass

    try:
        for (x, y, r) in circles_pink[0]:
            cv2.circle(frame, (x, y), r, (0, 255, 0), 2)
            cv2.circle(frame, (x, y), 2, (0, 255, 255), 3)
    except:
        pass

    cv2.putText(frame, str(theta), (300, 50), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 0), 2, lineType=cv2.LINE_AA)
    cv2.imshow(CALC_WINDOW_NAME, frame)
    #CSVに時間とその時のtheta情報を書き込む。
    save_data(count*1./30., theta)
    rec.write(frame)

    # ESCキーで終了する
    key = cv2.waitKey(INTERVAL)
    if key == ESC_KEY:
        break

    # 次のフレームの読み込み
    end_flag, frame = cap.read()
    count += 1.0

#終了処理
f.close()
rec.release()
cap.release()
cv2.destroyAllWindows()