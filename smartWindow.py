import os, sys,time # argv[1] is window status
import subprocess
import threading
import socket
import keyboard

W1=0.005; W2=1.1; W3=0.002; W4=0.0
sensor_result = [ False, False, 0.0, False, 0.0 , 0.0 , False, 0.0, 0.0,0.0]
window_status = "1"
motor_status = "0"
film_status = "0"
motion_status = False
#################### 디버 그나중 에삭 제####################
window_conf = open("debug_conf.txt",'r')
setter = window_conf.readline()
window_conf.close()
user_conf = []
user_conf.append(float(setter[0:3]))
user_conf.append(float(setter[3:5]))

def GaussianNomalization(x,mean,deviation,K=3) :
	print('x = %f mean = %f '%(x,mean))
	return ((x - mean) / (K * deviation))

def makeString() :
	try :
		w = open("./window_status.txt","r")
		window_status = w.readline()
		w.close()
		return "%d %d %d %d %d %d %d %d %d %d %d %d"%(int(sensor_result[0]), int(sensor_result[1]), int(sensor_result[2]), int(sensor_result[3]), int(sensor_result[4]), int(sensor_result[5]), int(sensor_result[6]), int(sensor_result[7]), int(sensor_result[8]), int(sensor_result[9]), int(motor_status), int(film_status))
	except :
		return "%d %d %d %d %d %d %d %d %d %d %d %d"%(int(sensor_result[0]), int(sensor_result[1]), int(sensor_result[2]), int(sensor_result[3]), int(sensor_result[4]), int(sensor_result[5]), int(sensor_result[6]), int(sensor_result[7]), int(sensor_result[8]), int(sensor_result[9]), 0 , int(film_status))

def Display() :
	print(makeString())

def decoding(args) :
	args = args
	result = args.decode()
	print(result)

def Set_configure(args) :
	global motion_status
	arg = args.split(' ')
	if arg[0] == "OPEN" :
		sensor_flag[2] = True
		output_flag[2] = True
		print("USER OPEN")
	elif arg[0] == "CLOSE" :
		sensor_flag[2] = False
		output_flag[2] = True
		print("USER CLOSE")
	elif arg[0] == "FILM" :
		if arg[1] == "1" :
			sensor_flag[3] = True
			output_flag[3] = True
			print("FLIM ON")
		elif arg[1] == "0" :
			sensor_flag[3] = False
			output_flag[3] = True
			print("FLIM CLOSE")
	elif arg[0] == "AUTO" :
		if arg[1] == "0" :
			output_flag[2] = True
			output_flag[3] = True
			print("UNSET AUTO")
		elif arg[1] == "1" :
			output_flag[2] = False
			output_flag[3] = False
			user_conf[0] = arg[2]
			user_conf[1] = arg[3]
			print("SET AUTO")
	elif arg[0] == "MOTION" :
		if arg[1] == "0" :
			motion_status = False
			print("MOTION OFF")
		elif arg[1] == "1" :
			motion_status = True
			print("MOTION ON")
	elif arg[0] == "GAS" :
		if arg[1] == "CLEAR" :
			sensor_flag[0] = False
			output_flag[0] = False
			sensor_result[0] = False
			sensor_result[7] = False
			print("gas clear")
	elif arg[0] == "CLEAR" :
		clear()	
		print("CLEAR")
	else :
		print("User Setting Value Error")
	
def Do_user_setting() :
	try:
		s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		print("소켓 생성완료")
	except socket.error as err :
    		print("에러 발생 원인 :  %s"%(err))
	try :
		HOST=''
		port=4321
		s.bind((HOST,port))
		while(True) :
			s.listen(5)
			print("%d 포트로 연결을 기다리는중"%(port))

			c, addr = s.accept()
			print(addr,"사용자가 접속함")
			Set_configure(c.recv(1024).decode())
			c.close()
	finally :
		c.close()

def Client() :
	s=socket.socker(socket.AF_INET,socket.SOCK_STREAM)
	
	port = 4321
	s.connect(('',port))
	decoding(s.recv(1024))
	s.close()

def Server() :
	try:
    		s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    		print("소켓 생성완료")
	except socket.error as err :
    		print("에러 발생 원인 :  %s"%(err))
	HOST=''
	port=1234
	s.bind((HOST,port))
	while(True) :
		temp=makeString()
		msg=bytearray(temp,'utf-8')

		s.listen(5)
		print("%d 포트로 연결을 기다리는중"%(port))

		c, addr = s.accept()
		print(addr,"사용자가 접속함")
		c.send(msg)
		c.close()
	

def SetConfig(sensor_flag,output_flag,before_setter, setter, where) :# 첫번째는 open/close status , 두번째는 user_config의 세팅 속성을 나타낸다. 세번째는 해당 list의 position을 나타낸다.
	if before_setter == str(setter) :
		return 
	moter_setter = (bool)(setter >> 1)	# int형을 list<bool>형태로 변경
	flim_setter  = (bool)(setter & 0b01)
	
	sensor_flag[where] = moter_setter
	output_flag[where] = True  # set user moter configure
	
	sensor_flag[where+1] = flim_setter
	output_flag[where+1] = True # set user flim configure

def SetGas(sensor_flag,output_flag) :
	gas_flag   = int(subprocess.check_output("python3 ./inner/MQ2.py 20",shell=True))
	smoke_flag = int(subprocess.check_output("python3 ./inner/MQ5.py 20",shell=True))
	if gas_flag == 1 : # else는 처리하지 않는다. 감지시 1set
		sensor_flag[0] = True
		output_flag[0] = True
		sensor_result[0] = True
	if smoke_flag == 1 :
		sensor_flag[0] = True
		output_flag[0] = True
		sensor_result[6] = True

def SetMotion(sensor_flag,output_flag) :
	if motion_status == False :
		output_flag[1] = False
		return 
	try :
		motion_flag = float(subprocess.check_output("python3 ./outer/ultrasonic_motion.py",shell=True))
		if motion_flag < 20.0 and motion_flag > 1.0 :
			sensor_flag[1] = True
			output_flag[1] = True
			sensor_result[3] = True
	except :
		motion_flag = -1
		sensor_result[3] = False
	
def SetUserConf(sensor_flag,output_flag,before_user_config,user_config) :
	user_config_file = open("user_conf.txt",'r')
	user_config = int(user_config_file.readline())
	Do_user_setting()
	SetConfig(sensor_flag,output_flag,before_user_config,user_config,2)

def SetRain(sensor_flag,output_flag) :
	rain_flag = int(subprocess.check_output("python3 ./outer/rain.py 20",shell=True))
	if rain_flag == 1 :
		sensor_flag[4] = True
		output_flag[4] = True
		sensor_result[1] = True
	else :
		sensor_flag[4] = False
		output_flag[4] = False
		sensor_result[1] = False

def SetDust(sensor_flag,output_flag,weights) :
    try :
        weightDust = float(subprocess.check_output("python3 ./outer/PMS7003.py 1",shell=True))
        sensor_result[7] = weightDust
        weights[0] = weightDust
    except :
        sensor_result[7] = -1.0
        weights[0] = -1.0

def SetDHT11_outer(sensor_flag,output_flag,weights) :
	while(True) :
		try :
			WO = (subprocess.check_output("python3 ./outer/dht11.py 1",shell=True))
			WTO = float(WO[5:10])
			WHO = float(WO[10:20])
			print("outer success")
		except :
			return	
		if WHO != -1 and WHO <=100 and WTO != -1 :
			weights[1] = WHO
			weights[2] = WTO
			sensor_result[8] = WHO
			sensor_result[9] = WTO
		

def SetDHT11_inner(sensor_flag,output_flag,weights) :
	while(True) :
		try :
			WI = (subprocess.check_output("python3 ./inner/dht11.py 1",shell=True))
			WTI = float(WI[5:10])
			WHI = float(WI[10:20])
			print("inner success")
		except :
			return
		if WHI != -1 and WHI <= 100 and WTI != -1 :
			weights[3] = WHI
			weights[4] = WTI
			sensor_result[4] = WHI
			sensor_result[5] = WTI


def SetLight(sensor_flag,output_flag,weights) :
	weightLight = float(subprocess.check_output("python3 ./outer/bh1750.py 2",shell=True))
	weights[5] = weightLight
	sensor_result[2] = round(weightLight,1)

def SetWeightedSum(sensor_flag,output_flag,weights) :
	weightDust = weights[0]
	WHO	= weights[1]
	WTO	= weights[2]
	WHI	= weights[3]
	WTI	= weights[4]
	weightLight=weights[5]

	gap = 1 - abs(GaussianNomalization(float(WHI),float(user_conf[0]),20.0,3))
	print(gap)
	WHG = 0.0
	if abs(WHI - WHO) >= 0.1 :
		if WHI <= 0.4 or WHI >= 0.6 :
			WHG = WHI - WHO
		else :
			WHG = 0
	#if (W1 * weightDust + W2 * WHG) > 1 :
	if (W1 * weightDust + W2 * gap ) > 1 :
		weighted_m_flag = True
	else :
		weighted_m_flag = False
	########### set WTG(WTGab = WTI(Weight Temperature Outer) - WTO(Weight Temperature Inner)), light
	WTG = WTI - WTO
	#if (W3 * weightLight + W4 * WHG) > 1 :
	gap = GaussianNomalization(float(WTI),float(user_conf[1]),1.5,3)
	print(gap)
	if (W3 * weightLight + W4 * gap) > 1 :
		weighted_f_flag = False
	else :
		weighted_f_flag = True
	if weighted_m_flag == True :
		sensor_flag[5] = True
		output_flag[5] = True
	else :
		sensor_flag[5] = False
		output_flag[5] = True
	if weighted_f_flag == True :
		sensor_flag[6] = True
		output_flag[6] = True
	else :
		sensor_flag[6] = False
		output_flag[6] = True

def limitSwitch() :
	while(True) :
		subprocess.check_output("python3 ./inner/limitSwitch.py",shell=True)


def SetWindow(sensor_flags,output_flags) :
	global motor_status
	global film_status
	while(True) :
		if output_flags[0] == True:
			motor_status = "1"
			subprocess.check_output("python3 ./inner/motor.py ccw",shell=True)
		elif output_flags[1] == True :
			motor_status = "0"
			subprocess.check_output("python3 ./inner/motor.py cw",shell=True)
		elif output_flags[2] == True :
			if sensor_flags[2] == True :
				motor_status = "1"
				subprocess.check_output("python3 ./inner/motor.py ccw",shell=True)
			else :
				motor_status = "0"
				subprocess.check_output("python3 ./inner/motor.py cw",shell=True)
		elif output_flags[4] == True :
			motor_status = "0"
			subprocess.check_output("python3 ./inner/motor.py cw",shell=True)
		elif output_flags[5] == True :
			if sensor_flags[5] == True :
				motor_status = "0"
				subprocess.check_output("python3 ./inner/motor.py cw",shell=True)
			else :
				motor_status = "1"
				subprocess.check_output("python3 ./inner/motor.py ccw",shell=True)

		if output_flags[3] == True :
			if sensor_flags[3] == True :
				subprocess.check_output("python3 ./inner/film.py on",shell=True)
				film_status = "1"
			else :
				subprocess.check_output("python3 ./inner/film.py off",shell=True)
				film_status = "0"
		elif output_flags[6] == True :
			if sensor_flags[6] == True :
				subprocess.check_output("python3 ./inner/film.py on",shell=True)
				film_status = "1"
			else :
				subprocess.check_output("python3 ./inner/film.py off",shell=True)
				film_status = "0"
	
before_user_config = "22"
user_config = "22"
sensor_flag = [ False, False,   False,      False,    False, False,          False ]	# 초기화
output_flag = [ False, False,   False,      False,    False, False,          False ]


weights = [0,0,0,0,0,0]	
thread = threading.Thread(target=SetWindow,args=(sensor_flag,output_flag))
thread.start()
thread = threading.Thread(target=limitSwitch,args=())
thread.start()
thread = threading.Thread(target=Server,args=())
thread.start()
thread = threading.Thread(target=Do_user_setting,args=())
thread.start()

output_flag[4] = False; output_flag[5] = False; output_flag[6] = False
threads_dht = []

t = threading.Thread(target=SetDHT11_outer,args=(sensor_flag,output_flag,weights))	
threads_dht.append(t)
t = threading.Thread(target=SetDHT11_inner,args=(sensor_flag,output_flag,weights))
threads_dht.append(t)
for th in threads_dht :
	th.start()

def clear() :
	global sensor_flag
	global output_flag
	global sensor_result
	for i in range(len(sensor_flag)) :
		sensor_flag[i] = False
	for i in range(len(output_flag)) :
		output_flag[i] = False
	for i in range(len(sensor_result)) :
		sensor_result[i] = False
	print("clear")
		


def interface() :
	while(True) :
		if keyboard.is_pressed(chr(27)) :
			clear()
			time.sleep(0.1)
t = threading.Thread(target=interface,args=())
t.start()


#############set gas############################
############### gas , motion, conf_moter, conf_film,  rain , weighted_moter, weighted_flim
try :
	while(True) :
		threads = []
		#SetGas(sensor_flag,output_flag)
		t = threading.Thread(target=SetGas,args=(sensor_flag,output_flag))
		threads.append(t)
		#############set motion#######################
		#SetMotion(sensor_flag,output_flag)
		t = threading.Thread(target=SetMotion,args=(sensor_flag,output_flag))
		threads.append(t)
		###########set user configure###########################
		#SetUserConf(sensor_flag,output_flag)
		#t = threading.Thread(target=SetUserConf,args=(sensor_flag,output_flag,before_user_config,user_config))

		#############set rain##############################
		#SetRain(sensor_flag,output_flag)
		t = threading.Thread(target=SetRain,args=(sensor_flag,output_flag))
		threads.append(t)

		############ set WHG(WHGab = WHO(Weight Humidity Outer) - WHI(Weight Humidity Inner)), dust

		t = threading.Thread(target=SetLight,args=(sensor_flag,output_flag,weights))
		threads.append(t)
		t = threading.Thread(target=SetDust,args=(sensor_flag,output_flag,weights))
		threads.append(t)
		for th in threads :
			th.start()
		for th in threads :
			th.join()
		
		Display()
		SetWeightedSum(sensor_flag,output_flag,weights)
		#SetWindow(sensor_flag,output_flag)
		before_user_config = str(user_config)

finally :
	user_config_file = open("user_conf.txt",'w')
	user_config_file.write("22")
	os.system("python3 ./inner/motor_stop.py")
	#os.system("python3 cleanup.py")
	user_config_file.close()








	









	
