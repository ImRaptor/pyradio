#!/usr/bin/python
import Adafruit_CharLCD as LCD
import atexit
import radio
import socket
import time
import xml.etree.cElementTree as ElTree
from subprocess import call

# Other vars to setup
lcd = LCD.Adafruit_CharLCDPlate()
running = True
rad = radio.Radio()
tree = ElTree.parse("/opt/radio/radioStations.xml")
stations = tree.getroot()
stationCount = len(stations)

def station_position(direction):
        stationPosition = int(stations.attrib["pos"])
        stationPosition += direction
        if stationPosition < 0:
                stationPosition = stationCount-1
        elif stationPosition > stationCount-1:
                stationPosition = 0
        stations.attrib['pos'] = str(stationPosition)
        tree.write("/opt/radio/radioStations.xml")
        return stationPosition

def change_station(direction):
        stationPosition = station_position(direction)
        rad.play_station(stations[stationPosition].text,stations[stationPosition].attrib['type'])
        lcd.clear()
        lcd.message(str(stationPosition))
        lcd.message("\n")
        lcd.message(stations[stationPosition].attrib['name'])

def network_detection(target="www.google.com", port="443"):
        try:
                host = socket.gethostbyname(target)
                s = socket.create_connection((host, port),2)
                return True
        except:
                pass
        return False

def mainloop():
        connTry = 0
        while running:
                #watch buttons
                if lcd.is_pressed(LCD.SELECT):
                        lcd.clear()
                        lcd.set_color(0,0,0)
                        call('halt', shell=False)
                elif lcd.is_pressed(LCD.LEFT):
                        lcd.clear()
                        #lcd.message("Left")
                        change_station(-1)
                elif lcd.is_pressed(LCD.DOWN):
                        lcd.clear()
                        lcd.message("Down")
                elif lcd.is_pressed(LCD.UP):
                        lcd.clear()
                        lcd.message("Up")
                elif lcd.is_pressed(LCD.RIGHT):
                        lcd.clear()
                        #lcd.message("Right")
                        change_station(1)
                if not rad.check_running() and connTry < 5:
                        connTry+=1
                        change_station(0)
                        time.sleep(2)
                elif connTry >=5 and not network_detection() and not network_detection(target="www.msn.ca",port="80"):
                        lcd.clear()
                        lcd.message("Connection\nproblem")
                else:
                        connTry=0
                time.sleep(0.1)

def startup():
        change_station(0)

def cleanup():
        rad._kill_screen()

if __name__ == "__main__":
        atexit.register(cleanup)
        startup()
        mainloop()