import os, sys
import getopt
import serial
import time
import datetime
import re
import thread
import smtplib
from email.mime.text import MIMEText
import noise.wsgi
from myapp.models import *


threshold = 70
emailtime = datetime.datetime.now()
firstemail = True

def device_exists(device):
	try:
		from serial.tools import list_ports

		for port in list_ports.comports():
			if port[0] == device:
				return True

		return False
	except:
		return os.path.exists(device)

def read_input():
	global cmdinput
	while (1):
		cmdinput = raw_input()

def shouldEmail():
        global firstemail
        if firstemail:
                return True
        d = datetime.timedelta(minutes = 15)
        if(d < datetime.datetime.now()-emailtime):
                return True
        else:
                return False

def email(node, dB):
        to = "<receiver_email>"
        gmail_user = "<sender_email>"
        gmail_password = "<sender_password>"
        smtpserver = smtplib.SMTP("smtp.gmail.com", 587)

        smtpserver.starttls()
        smtpserver.login(gmail_user, gmail_password)

        message = "Node located at ((%s)) is showing elevated noise levels of %s dB" % (node, dB)
        msg = MIMEText(message)
        msg['Subject'] = "Noise Alert!"
        msg["From"] = gmail_user
        msg["To"] = to
        smtpserver.sendmail(gmail_user, [to], msg.as_string())
        smtpserver.quit()
        global firstemail
        if firstemail:
                firstemail = False
        emailtime = datetime.datetime.now()
        

def uploadData(data):
        uploadTime = timezone.now()
        for key in data:
                location = Node.objects.get(location=key)
                location.current = data[key]
                location.save()
                reading = Reading(node=location, time=uploadTime, db_level=data[key])
                reading.save()
                if(data[key] > threshold):
                        if shouldEmail():
                                email(location.location, data[key])

def parseData(reading):
        reading_nospace = re.findall(r'([a-zA-Z]|[0-9]|[#:$])', reading)
        reading = ""
        for letter in reading_nospace:
                reading+=letter
        if(reading[0] != "#"):
                return
        else:
                nodes = re.findall(r'[a-z]+', reading)
                dB = re.findall(r'\d[0-9]*', reading)
                dB = map(int, dB)
                data = {}
                i = 0
                for node in nodes:
                        data[node] = dB[i]
                        i+=1
                print(data)
                uploadData(data)
                

def readSerial():

    #initialize Serial
    sd = serial.Serial()
    sd.port="/dev/ttyACM0"
    sd.baudrate=9600
    sd.bytesize=serial.EIGHTBITS
    sd.parity=serial.PARITY_NONE
    sd.stopbits=serial.STOPBITS_ONE
    sd.xonxoff=False
    sd.rtscts=False
    sd.dsrdtr=False
    sd.timeout=1
    force = False
    show_time = 0
    show_systime = 0
    basepat = ""
    instantpat = ''
    quitpat = ''
    basetime = 0
    instanttime = None
    endtime = 0
    outputfile = None
    command = ""
    skip_device_check = 0

    if force:
    	toggle = sd.xonxoff
    	sd.xonxoff = not toggle
    	sd.open()
    	sd.close()
    	sd.xonxoff = toggle
    sd.open()
    sd.flushInput()
    sd.flushOutput()
    time.sleep(1)

    while(1):
        try:
            data = sd.read()
            if(data == "#"):
                reading = "#"
                while(data != "$"):
                        data = sd.read()
                        reading += data
                parseData(reading)
                sd,flush()
            else:
                continue
        except:
            continue

    sd.close()
    sys.stdout.flush()

    
            
if __name__=="__main__":
        readSerial()
            
            
