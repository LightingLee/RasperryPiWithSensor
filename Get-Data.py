import csv
import json
import datetime
import micropyGPS
import bm280
import luxsensor
import threading
import serial
import time
import uvsi1145
import C2Python

Write_Freq = 1 #The freq to write log. Min as 1 sec
Sendfreq = 10 #The freq to write log. Min as 1 sec

def rungps():
    while True:
        try:
            s = serial.Serial('/dev/serial0', 9600, timeout=10)
        except:
            continue
        else:
            break
    s.readline()
    while True:
        sentence = s.readline().decode('utf-8')
        if sentence[0] != '$':
            continue
        for x in sentence:
            gps.update(x)

def runbm280():
    bm280.setbm280()
    while True:
        try:
            bm280.readData()
            time.sleep(3)
        except:
            print 'Read BM280 ERROR'
            continue

def runtsl2561():
    while True:
        try:
            light.readData()
            time.sleep(3)
        except:
            print 'Read lux ERROR'
            continue

def runsi1145():
    while True:
        try:
            uv.readData()
            time.sleep(3)
        except:
            print 'Read UV Index ERROR'
            continue

"""

Start to start data collect thread of each sensor

"""

gps = micropyGPS.MicropyGPS(9, 'dd')
gpsthread = threading.Thread(target=rungps, args=())
gpsthread.daemon = True
gpsthread.start()

bm280 = bm280.BM280()
bm280thread = threading.Thread(target=runbm280, args=())
bm280thread.daemon = True
bm280thread.start()

light = luxsensor.light2561()
lightthread = threading.Thread(target=runtsl2561, args=())
lightthread.daemon = True
lightthread.start()

uv = uvsi1145.uv1145()
uvthread = threading.Thread(target=runsi1145, args=())
uvthread.daemon = True
uvthread.start()

"""

end to start data collect thread of each sensor

"""

#C2Python.C2Python_init()
#start = time.time()

while True:
    time.sleep(Write_Freq)

    print '=============Write Data==============='
    h = gps.timestamp[0] if gps.timestamp[0] < 24 else gps.timestamp[0] - 24
    time_gps = '%2d:%02d:%04f' % (h, gps.timestamp[1], gps.timestamp[2])
    print 'Data is ', date
    print 'Time is ', time_gps
    print 'UV is ', uv.uv_index

    with open('/home/pi/project/EV-eye/data/data.csv', 'a') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow([date_gps,time_gps, \
                         bm280.temp, bm280.pres, bm280.hum, \
                         light.lux, uv.uv_index, \
                         gps.latitude[0],gps.longitude[0],])

"""
    if ( (time.time() - start) >= Sendfreq ):
        send_data = "{" \
                    + "\"Date\":\"" + date_gps + "\","\
                    + "\"Time\":" + str(time_gps) + ","\
                    + "\"Temp\":" + str(bm280.temp) + ","\
                    + "\"Pres\":" + str(bm280.pres) + ","\
                    + "\"Hum\":" + str(bm280.hum) + ","\
                    + "\"Vis\":" + str(light.lux) + ","\
                    + "\"UVIn\":" + str(uv.uv_index) + ","\
                    + "\"Lat\":" + str(gps.latitude[0]) + ","\
                    + "\"Lon\":" + str(gps.longitude[0]) \
                    + "}"
        with open('/home/pi/project/EV-eye/data/send_cache.csv', 'a') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow([date,time_gps, \
                             bm280.temp, bm280.pres, bm280.hum, \
                             light.lux, uv.uv_index, \
                             gps.latitude[0],gps.longitude[0]])

"""
