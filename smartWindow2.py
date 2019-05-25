import os, sys, time # argv[1] is window status
import subprocess
import threading

W1=1.0; W2=1.0; W3=1.0; W4=1.0
sensor_result = [ False, False, 0.0, 0.0, 0.0 , 0.0 , False, 0.0, 0.0,0.0]

def Display() :
	print("smoke = " + str(sensor_result[1]))
	print("rain = " + str(sensor_result[1]))
	print("light = " + str(sensor_result[2]))
	print("disdance = " + str(sensor_result[3]))
	print("inner humi = " + str(sensor_result[4]))
	print("inner temp = " + str(sensor_result[5]))
	print("gas = " + str(sensor_result[6]))
	print("dust = " + str(sensor_result[7]))
	print("outer humi = " + str(sensor_result[8]))
	print("outer temp = " + str(sensor_result[9]))

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
	if gas_flag == 1 or smoke_flag == 1 : # else는 처리하지 않는다. 감지시 1set
		sensor_flag[0] = True
		output_flag[0] = True
		sensor_result[0] = True
		sensor_result[6] = True
	print("success gas")	

def SetMotion(sensor_flag,output_flag) :
	motion_flag = float(subprocess.check_output("python3 ./outer/ultrasonic_motion.py",shell=True))
	if motion_flag < 20.0 :
		sensor_flag[1] = True
		output_flag[1] = True
	sensor_result[3] = motion_flag
	print("success motion")
	
def SetUserConf(sensor_flag,output_flag,befoe_user_config,user_config) :
	user_config_file = open("user_conf.txt",'r')
	user_config = int(user_config_file.readline())
	SetConfig(sensor_flag,output_flag,before_user_config,user_config,2)
	print("success userConfig")	

def SetRain(sensor_flag,output_flag) :
	rain_flag = int(subprocess.check_output("python3 ./outer/rain.py 20",shell=True))
	if rain_flag == 1 :
		sensor_flag[4] = True
		output_flag[4] = True
		sensor_result[1] = True
	else :
		sensor_result[1] = False
	print("success rain")

def SetDust(sensor_flag,output_flag,weights) :
	weightDust = float(subprocess.check_output("python3 ./outer/PMS7003.py 1",shell=True))
	sensor_result[7] = weightDust
	weights[0] = weightDust
	print("success dust")

def SetDHT11_outer(sensor_flag,output_flag,weights) :
	WO = (subprocess.check_output("python3 ./outer/dht11.py 1",shell=True))
	WHO = float(WO[5:10])
	WTO = float(WO[15:20])
	weights[1] = WHO
	weights[2] = WTO
	sensor_result[8] = WTO
	sensor_result[9] = WHO
	
	print("success DHT_outer")

def SetDHT11_inner(sensor_flag,output_flag,weights) :
	WI = (subprocess.check_output("python3 ./inner/dht11.py 1",shell=True))
	WHI = float(WI[5:10])
	WTI = float(WI[15:20])
	weights[3] = WHI
	weights[4] = WTI
	sensor_result[4] = WTI
	sensor_result[5] = WHI

	print("success DHT_inner")

def SetLight(sensor_flag,output_flag,weights) :
	weightLight = float(subprocess.check_output("python3 ./outer/bh1750.py 2",shell=True))
	weights[5] = weightLight
	sensor_result[2] = weightLight
	print("success Light")

def SetWeightedSum(sensor_flag,output_flag,weights) :
	weightDust = weights[0]
	WHO	= weights[1]
	WTO	= weights[2]
	WHI	= weights[3]
	WTI	= weights[4]
	weightLight=weights[5]

	WHG = 0.0
	if abs(WHI - WHO) >= 0.1 :
		if WHI <= 0.4 or WHI >= 0.6 :
			WHG = WHI - WHO
		else :
			WHG = 0
	if (W1 * weightDust + W2 * WHG) > 1 :
		weighted_m_flag = True
	else :
		weighted_m_flag = False
	########### set WTG(WTGab = WTI(Weight Temperature Outer) - WTO(Weight Temperature Inner)), light
	WTG = WTI - WTO
	if (W3 * weightLight + W4 * WHG) > 1 :
		weighted_f_flag = True
	else :
		weighted_f_flag = False
	if weighted_m_flag == True :
		if sensor_flag[5] != weighted_m_flag :
			sensor_flag[5] = True
			output_flag[5] = True
	else :
		if sensor_flag[5] != weighted_m_flag :
			sensor_flag[5] = False
			output_flag[5] = True
		if weighted_f_flag == True :
			if sensor_flag[6] != weighted_f_flag :
				sensor_flag[6] = True
				output_flag[6] = True
		else :
			if sensor_flag[6] != weighted_f_flag :
				sensor_flag[6] = False
				sensor_flag[6] = True

	print("success weighted sum")

def limitSwitch() :
    os.system("python3 ./inner/limitSwitch.py")

def SetWindow(sensor_flags,output_flags) :
	if output_flags[0] == True:
		os.system("python3 ./inner/motor.py ccw")
		print("reason gas")
	elif output_flags[1] == True :
		os.system("python3 ./inner/motor.py cw")
		print("reason motion")
	elif output_flags[2] == True :
		if sensor_flags[2] == True :
			os.system("python3 ./inner/motor.py ccw")
		else :
			os.system("python3 ./inner/motor.py cw")
		print("reason user conf")
	elif output_flags[4] == True :
		os.system("python3 ./inner/motor.py cw")
		print("reason rain")
	elif output_flags[5] == True :
		if sensor_flags[5] == True :
			os.system("python3 ./inner/motor.py cw")
		else :
			os.system("python3 ./inner/motor.py ccw")
		print("reason weighted sum")

	if output_flags[3] == True :
		if sensor_flags[3] == True :
			os.system("python3 ./inner/film.py on")
		else :
			os.system("python3 ./inner/film.py off")
	elif output_flags[6] == True :
		if sensor_flags[6] == True :
			os.system("python3 ./inner/film.py on")
		else :
			os.system("python3 ./inner/film.py off")
	

before_user_config = "22"
user_config = "22"
sensor_flag = [ False, False,   False,      False,    False, False,          False ]	# 초기화
output_flag = [ False, False,   False,      False,    False, False,          False ]


############### gas , motion, conf_moter, conf_film,  rain , weighted_moter, weighted_flim
try :
	while(True) :
		output_flag[4] = False; output_flag[5] = False; output_flag[6] = False
		threads = []
		thread = threading.Thread(target=limitSwitch,args=())
		thread.start()
		#############set gas############################
		#SetGas(sensor_flag,output_flag)
		t = threading.Thread(target=SetGas,args=(sensor_flag,output_flag))
		threads.append(t)
		#############set motion#######################
		#SetMotion(sensor_flag,output_flag)
		t = threading.Thread(target=SetMotion,args=(sensor_flag,output_flag))
		threads.append(t)
		###########set user configure###########################
		#SetUserConf(sensor_flag,output_flag)
		t = threading.Thread(target=SetUserConf,args=(sensor_flag,output_flag,before_user_config,user_config))
		threads.append(t)

		#############set rain##############################
		#SetRain(sensor_flag,output_flag)
		t = threading.Thread(target=SetRain,args=(sensor_flag,output_flag))
		threads.append(t)

	############ set WHG(WHGab = WHO(Weight Humidity Outer) - WHI(Weight Humidity Inner)), dust
		weights = [0,0,0,0,0,0]	

		t = threading.Thread(target=SetDust,args=(sensor_flag,output_flag,weights))
		threads.append(t)
		t = threading.Thread(target=SetDHT11_outer,args=(sensor_flag,output_flag,weights))
		threads.append(t)
		t = threading.Thread(target=SetDHT11_inner,args=(sensor_flag,output_flag,weights))
		threads.append(t)
		t = threading.Thread(target=SetLight,args=(sensor_flag,output_flag,weights))
		threads.append(t)

		for th in threads :
			th.start()
		for th in threads :
			th.join()
		Display()
		SetWeightedSum(sensor_flag,output_flag,weights)
		
		print(sensor_flag)
		print(output_flag)
		SetWindow(sensor_flag,output_flag)
		before_user_config = str(user_config)

except KeyboardInterrupt :
	print("end")	
	
finally :
	user_config_file = open("user_conf.txt",'w')
	user_config_file.write("22")
	user_config_file.close()








	









	
