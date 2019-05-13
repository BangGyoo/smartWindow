import os, sys, time # argv[1] is window status

W1=1.0; W2=1.0; W3=1.0; W4=1.0

def SetConfig(sensor_flag,output_flag, setter, where) :# 첫번째는 open/close status , 두번째는 user_config의 세팅 속성을 나타낸다. 세번째는 해당 list의 position을 나타낸다.
	moter_setter = (bool)(setter >> 1)	# int형을 list<bool>형태로 변경
	flim_setter  = (bool)(setter)
	if sensor_flag[where] != moter_setter :
		sensor_flag[where] = moter_setter
		output_flag[where] = True  # set user moter configure
	if sensor_flag[where+1] != flim_setter :
		sensor_flag[where+1] = flim_setter
		output_flag[where+1] = True # set user flim configure

def SetWindow(sensor_flags,output_flags) :
	if output_flags[0] == True :
		os.system("python3 ./inner/motor_cw_ccw.py cw 23")
	elif output_flags[1] == True :
		os.system("python3 ./inner/motor_cw_ccw.py ccw 23")
	elif output_flags[2] == True :
		if sensor_flags[2] == True :
			os.system("python3 ./inner/motor_cw_ccw.py cw 23")
		else :
			os.system("python3 ./inner/motor_cw_ccw.py ccw 23")
	elif output_flags[4] == True :
		os.system("python3 ./moter_on_off.py cw 23")
	elif output_flags[5] == True :
		if sensor_flags[5] == True :
			os.system("python3 ./inner/motor_cw_ccw.py cw 23")
		else :
			os.system("python3 ./inner/motor_cw_ccw.py ccw 23")

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
	



sensor_flag = [ False, False,   False,      False,    False, False,          False ]	# 초기화
output_flag = [ False, False,   False,      False,    False, False,          False ]
############### gas , motion, conf_moter, conf_film,  rain , weighted_moter, weighted_flim
i = 1
try :
	while i < 5 :
		i+=1
		#############set gas############################
		gas_flag   = int(os.system("python3 ./inner/MQ2.py 20"))
		smoke_flag = int(os.system("python3 ./inner/MQ5.py 20"))
		if gas_flag == 1 or smoke_flag == 1 : # else는 처리하지 않는다. 감지시 1set
			sensor_flag[0] = True
			output_flag[0] = True
		#############set motion#######################
		motion_flag = int(os.system("python3 ./outer/motion.py 20"))
		if motion_flag == 1 :
			sensor_flag[1] = True
			output_flag[1] = True
		###########set user configure############################
		user_config_file = open("user_conf.txt",'r')
		user_config = int(user_config_file.readline())

		SetConfig(sensor_flag,output_flag,user_config,2)
		rain_flag = int(os.system("python3 ./outer/rain.py 20"))
		#############set rain##############################
		if rain_flag == 1 :
			sensor_flag[4] = True
			output_flag[4] = True
		############ set WHG(WHGab = WHO(Weight Humidity Outer) - WHI(Weight Humidity Inner)), dust
		weightDust = float(os.system("python3 ./outer/PMS7003.py 20"))
		WHO = float(os.system("python3 ./outer/dht11.py 20"))
		WHI = float(os.system("python3 ./inner/dht11.py 20"))
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
		weightLight = float(os.system("python3 ./outer/light.py 20"))
		WTO = float(os.system("python3 ./outer/dht11.py 20"))
		WTI = float(os.system("python3 ./inner/dht11.py 20"))
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
		
		SetWindow(sensor_flag,output_flag)
	'''	
		users = SearchUser()
		for user in users :
			if !(push_msg_flags) :
				pushMassage()
	'''
except KeyboardInterrupt :
	print("end")	
	









	









	
