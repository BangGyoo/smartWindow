import os, sys, time # argv[1] is window status
import subprocess

W1=1.0; W2=1.0; W3=1.0; W4=1.0

def SetConfig(sensor_flag,output_flag,before_setter, setter, where) :# 첫번째는 open/close status , 두번째는 user_config의 세팅 속성을 나타낸다. 세번째는 해당 list의 position을 나타낸다.
	if before_setter == str(setter) :
		return 
	moter_setter = (bool)(setter >> 1)	# int형을 list<bool>형태로 변경
	flim_setter  = (bool)(setter & 0b01)
	
	sensor_flag[where] = moter_setter
	output_flag[where] = True  # set user moter configure
	
	sensor_flag[where+1] = flim_setter
	output_flag[where+1] = True # set user flim configure

def SetWindow(sensor_flags,output_flags) :
	print("debug")
	if output_flags[0] == True:
		os.system("python3 ./inner/motor_lmt.py ccw")
	elif output_flags[1] == True :
		os.system("python3 ./inner/motor_lmt.py cw")
	elif output_flags[2] == True :
		if sensor_flags[2] == True :
			os.system("python3 ./inner/motor_lmt.py ccw")
		else :
			os.system("python3 ./inner/motor_lmt.py cw")
	elif output_flags[4] == True :
		os.system("python3 ./inner/motor_lmt.py cw")
	elif output_flags[5] == True :
		if sensor_flags[5] == True :
			os.system("python3 ./inner/motor_lmt.py cw")
		else :
			os.system("python3 ./inner/motor_lmt.py ccw")

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
sensor_flag = [ False, False,   False,      False,    False, False,          False ]	# 초기화
############### gas , motion, conf_moter, conf_film,  rain , weighted_moter, weighted_flim
try :
	while(True) :
		output_flag = [ False, False,   False,      False,    False, False,          False ]
		#############set gas############################
		gas_flag   = int(subprocess.check_output("python3 ./inner/MQ2.py 20",shell=True))
		smoke_flag = int(subprocess.check_output("python3 ./inner/MQ5.py 20",shell=True))
		if gas_flag == 1 or smoke_flag == 1 : # else는 처리하지 않는다. 감지시 1set
			sensor_flag[0] = True
			output_flag[0] = True
		#############set motion#######################
		motion_flag = float(subprocess.check_output("python3 ./outer/ultrasonic_motion.py",shell=True))
		print(motion_flag)
		if motion_flag < 20.0 :
			sensor_flag[1] = True
			output_flag[1] = True
		###########set user configure############################
		user_config_file = open("user_conf.txt",'r')
		user_config = int(user_config_file.readline())
		SetConfig(sensor_flag,output_flag,before_user_config,user_config,2)
		

		rain_flag = int(subprocess.check_output("python3 ./outer/rain.py 20",shell=True))
		#############set rain##############################
		if rain_flag == 1 :
			sensor_flag[4] = True
			output_flag[4] = True
		############ set WHG(WHGab = WHO(Weight Humidity Outer) - WHI(Weight Humidity Inner)), dust
		weightDust = float(subprocess.check_output("python3 ./outer/PMS7003.py 1",shell=True))
		WO = (subprocess.check_output("python3 ./outer/dht11.py 1",shell=True))
		WHO = float(WO[5:10])
		
		WTO = float(WO[15:20])
		WI = (subprocess.check_output("python3 ./inner/dht11.py 1",shell=True))
		WHI = float(WI[5:10])
		WTI = float(WI[15:20])
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
		weightLight = float(subprocess.check_output("python3 ./outer/bh1750.py 2",shell=True))
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








	









	
