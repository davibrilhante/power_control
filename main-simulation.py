import numpy as np
import scipy as sc
import simpy as sp
import simutime as st




def powerControlAlgorithm(rssi, txpower, offset):
    1

def ltePowerControl():
    1

def channel(object):
    def __init__(self, Type='WITHOUT_NOISE', dist=0, freq=700e6, bw=400e6):
        self.pathLoss = 0
        self.bandwidth = bw
        self.centerFreq = freq
        self.type = Type

    def sendMessage(self, Input, Output):
        1


class battery(int):
    def __init__(self,voltage=3,drawncurrent=200):
        self.charge=voltage*drawncurrent*3.6

    def sendMessage(self, spent):
        self.charge -= 1e-6

    def receiveMessage(self, spent):
        self.charge -= 1e-6

    def stayAwake(self, spent, time):
        self.charge -= 1e-6*time

    def stayAsleep(self, spent, time):
        self.charge -= 1e-6*time

class message(str):
    def __init__(self, payload=None)
        self.payload = payload
        self.status = None

    def loremIpsum(self, length):
        lorem = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed '+\
        'id mauris semper, dapibus elit at, laoreet leo. Nullam sed facilisis '+\
        'orci. Donec vitae est metus. Cras sollicitudin augue lacus, sed aliquet'+\
        ' nisi bibendum nec. Sed in aliquet quam. Class aptent taciti sociosqu ad'+\
        ' litora torquent per conubia nostra, per inceptos himenaeos. Sed tempus '+\
        'libero laoreet vehicula lacinia. Nunc commodo ut sem in lobortis. Nunc '+\
        'euismod dapibus malesuada. Aliquam quis dictum dui. Donec nisl orci, '+\
        'vulputate eu tempor vel, volutpat vitae lacus. Vestibulum ante ipsum '+\
        'primis in faucibus orci luctus et ultrices posuere cubilia Curae; In hac'+\
        ' habitasse platea dictumst.Quisque non dolor ac lacus tincidunt blandit. '+\
        'Aliquam malesuada ex vitae elementum viverra. Morbi eros eros, commodo eu '+\
        'turpis eu, ornare iaculis orci. Nulla iaculis augue eget quam consequat, '+\
        'ut sodales lacus finibus. Duis malesuada neque non ligula pretium, sed '+\
        'cursus ex convallis. In non mollis nisi, quis ullamcorper nunc. Sed elementum est vel nisi dapibus posuere.'

        self.payload = lorem[:length]

class scenario(object):
    def __init__(self, radius=1000, net=None):
        self.radius = radius
        self.network = net
        self.sensors = []
        self.channel = channel()
    def send(self, transmitter, receiver)

    def spreadsensors(self, nsensors):
        check = []
        while len(check) != nsensors:
            sens = sensor(self.radius,0,len(check+1))
            if check.count([sens.x, sens.y]) == 0:
                self.sensors.append(sens)
                check.append([sens.x, sens.y])

    
        

class sensor(object):
    def __init__(self,radius=1000, gain=0, Id=1, scenario = None):
        self.x=radius
        self.y=radius
        self.txPower=10
        self.period = 1 #1 hour
        self.lifecycle = {
            'awake':10 #seconds
            'sleep':10*60 - 10 #seconds
            }

        self.id = Id
        self.battery = battery()
        self.scenario = scenario

        while self.x**2 + self.y**2 > radius:
            self.x = np.random.uniform(-radius, radius)
            self.y = np.random.uniform(-radius, radius)

    def setMessagePeriod(self, period):  
        self.period = period

    def sendMessage(self):
        1

    

    

class network(object):
    def __init__(self, power=30,env=None):
        self.txPower = power
        self.bandwith = 400e6 #hertz
        self.centerFreq = 700e6 #hertz

        self.sensibility = -110 #dBm


if __name__=="__main__":
    simtime = 10
    env = sp.Environment()
    msg = message
    env.run(simtime)
