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


