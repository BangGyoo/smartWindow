def Setconfig(sensor_flag, setter, where) :
    flags = setter << where
    sensor_flag &= flags
W1=0.0,W2=0.0,W3=0.0,W4=0.0

import os, sys, time # argv[1] is window status
import enum

class WIN_STATUS(enum.Enum) :
    MOTOR = 0b10
    FLIM  = 0b01

class SENSOR_FLAG(enum.Enum) :
    GAS        = 0b1000000
    MOTION     = 0b0100000
    USER_MOTOR = 0b0010000
    USER_FLIM  = 0b0001000
    RAIN       = 0b0000100
    WEIGHTED_M = 0b0000010  #Weighted sum flag, ver.Motor
    WEIGHTED_F = 0b0000001  #weighted sum flag, ver.Flim

window_status = int(sys.argv[1]) # 첫번째 인자
timer_motor   = int(sys.argv[2]) # 두번째 인자
push_msg_flag = int(sys.argv[3]) # 세번째 인자, true or false이다.
sensor_flag   = int(sys.flag[4]) # 네번째 인자

gas_flag   = int(os.system("python ./inner/MQ2.py 20"))
smoke_flag = int(os.system("python ./inner/MQ5.py 20"))
if gas_flag == 1 or smoke_flag == 1 :
    sensor_flag = sensor_flag | SENSOR_FLAG.GAS     # else는 처리하지 않는다. 감지시 1set

motion_flag= int(os.system("python ./outer/motion.py 20"))
if motion_flag == 1 :
    sensor_flag = sensor_flag | SENSOR_FLAG.MOTION  # else는 처리하지 않는다. 감지시 1set

user_config_file = open("여기에 경로 적어야 함.txt",r)
user_config = int(user_config_file.readline())
############# 임시 제작 #########################

SetConfig(sensor_flag, user_config,3)
rain_flag = int(os.system("python ./outer/rain.py 20")
if rain_flag == 1 :
    sensor_flag = sensor_flag | SENSOR_FLAG.RAIN

weightDust = float(os.system("python ./outer/PMS7003.py 20"))
WHO = float(os.system("python ./outer/dht11.py 20")) #WHO is Weight Huminity outer
WHI = float(os.system("python ./inner/dht11_2.py 20")) # WHI is Weight Huminity inner
if abs(WHI - WHO) >= 0.1 :
    if WHI <= 0.4 || WHI >= 0.6 :
        WHG = WHI - WHO
if (W1 * weightDust + W2 * WHG) > 1 :
    weighted_m_flag = 1
else :
    weighted_m_flag = 0

weightLight = float(os.system("python ./outer/light.py 20"))
WTO = float(os.system("python ./outer/dht11.py 20"))
WHI = float(os.system("python ./inner/dht11.py 20"))
WHG = WHI - WTO # Weight Temperature Gap = weight temperature inner - weight temperature outer
if (W3 * weightLight + W4 * WHG) > 1 :
    weighted_f_flag = 1
else :
    weighted_f_flag = 0

if weighted_m_flag == 1 :
    sensor_flag = sensor_flag | SENSOR_FLAG.WEIGHTED_M
if weighted_f_flag == 1 :
    sensor_flag = sensor_flag | SENSOR_FLAG.WEIGHTED_F


SetWindow(sensor_flag)
users = SearchUser()
for user in users :
    if !(push_msg_flags) :
        pushMassage()


 














