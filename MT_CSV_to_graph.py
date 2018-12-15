import matplotlib
import matplotlib.pyplot as plt

#データの扱いに必要なライブラリ
import pandas as pd
import numpy as np
import datetime as dt

#グラフを綺麗に表現--------------------
plt.style.use('ggplot')
font = {'family': 'meiryo'}
matplotlib.rc('font', **font)
#------------------------------------

#------------------------------------
#ArduinoサイドのCSVを読み込む
#Arduinoは時間と気圧センサーの値が書き込まれている。
Ard_CSV = "./time_pa/time_and_pa_slow.csv"
"""
Ard_val = pd.read_csv(Ard_CSV, names=['time', 'hpa'])
print(len(Ard_val))
plt.plot(Ard_val['time'], Ard_val['hpa'], label = 'ard')
#plt.show()
"""

Ard_val = pd.read_csv(Ard_CSV)
Ard_val = Ard_val.values
plt.plot(Ard_val[:, 0], Ard_val[:, 1])
plt.show()
#-------------------------------------
#-------------------------------------
#MovieサイドのCSVを読み込む
#Movieでは時間とその時の角度が書き込まれている。
Mov_CSV = "./data/data_slow_FHD.csv"
"""
Mov_val = pd.read_csv(Mov_CSV, names=['time', 'bend'])
print(len(Mov_val))
plt.plot(Mov_val['time'], Mov_val['bend'], label='mov')
#plt.show()
"""

Mov_val = pd.read_csv(Mov_CSV)
Mov_val = Mov_val.values
plt.plot(Mov_val[:,0], Mov_val[:, 1])
plt.show()

#-------------------------------------
#--------------------------------------
#ArduinoとMovieのグラフを合わせたグラフをかく。
#同じ時間のタイミングで横軸にBending 縦軸にhpaをセットする。

#両方の配列を揃える。
hpa = Ard_val[:,1]
bending_deg = Mov_val[:,1]

print(hpa)
print("------------------")
#print(bending_deg)

#二つのCSVファイルのリストの長さを揃える操作
if(len(hpa) > len(bending_deg)):
    hpa = hpa[0:len(bending_deg)]

elif(len(hpa) < len(bending_deg)):
    bending_deg = bending_deg[0 : len(hpa)]

print(len(hpa))
print(len(bending_deg))

#最小二乗近似で直線の方程式を求める。
print(np.polyfit(hpa, bending_deg, 1))
#一次の式を求める。
func = np.poly1d(np.polyfit(hpa, bending_deg, 1))(hpa)


plt.plot(hpa, func, label='d=1')

#グラフ画像の保存
filename = 'hpa_bending_line'
plt.savefig("./graph/" + filename + '.png')
#横軸にhpa 縦軸にbending_degのグラフを作成。
#気圧センサーのhpaからその時のbending_degを想定できる方程式を作成したい。
plt.plot(hpa, bending_deg)
plt.show()