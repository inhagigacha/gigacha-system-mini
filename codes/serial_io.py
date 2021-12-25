# -*- coding:utf-8 -*-
import serial
import numpy as np
from time import sleep

class SerialIO:
    def __init__(self):
        self.speed = 555 #0~800
        self.steer = 1800 #1300 ~ 1800. middle = 1550
        self.brake = 0 #1200~1500
        self.direction = 0 #0 or 1


        self.serial1 = serial.Serial(port='/dev/ttyUSB0', baudrate=115200)
        

    def serWrite(self):
        self.serial1.write(self.writeBuffer())
    
    def writeBuffer(self):
        packet = []

        direction = self.direction

        # 타입 맞춰주기
        speed = np.uint16(self.speed)
        steer = np.uint16(self.steer)
        brake = np.uint16(self.brake)

        # 바이트 분할 작업
        speed_L = speed & 0xff
        speed_H = speed >> 8

        steer_L = steer & 0xFF
        steer_H = steer >> 8

        brake_L = brake & 0xff
        brake_H = brake >> 8

        # CLC 계산을 위한 바이트 총합 구하기
        sum_c = direction + speed_L + speed_H + steer_L \
                    + steer_H + brake_L + brake_H + 13 + 10

        # CLC는 1 Byte
        clc = np.uint8(~sum_c)

        packet.append(0x53)
        packet.append(0x54)
        packet.append(0x58)
        packet.append(direction)
        packet.append(speed_L)
        packet.append(speed_H)
        packet.append(steer_L)
        packet.append(steer_H)
        packet.append(brake_L)
        packet.append(brake_H)
        packet.append(0x00)
        packet.append(0x0D)
        packet.append(0x0A)
        packet.append(clc)

        return packet       
    def run(self):
        self.serWrite() 

if __name__ == "__main__":
    sio = SerialIO()
    while True:
        sio.run()
        sleep(0.1)