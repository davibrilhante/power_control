import sys
import numpy as np
import scipy as sc
import simpy as sp
import simutime as st
from commpy import modulation as mod
from commpy import channels as ch
from commpy import channelcoding
from commpy import utilities as utils
'''
from gnuradio import blocks
from gnuradio import fft
from gnuradio import channels
from gnuradio import digital
from gnuradio import fec
import gnuradio as gr
import physical-layer as phy
'''
SEED = int(sys.argv[1])
np.random.seed(SEED)

CENTER_FREQ=700e6
BANDWIDTH = 40e6
SIMULATION_TIME=st.seconds(24*3600)



def sensorTPCAlgorithm(txPower, rxPower, rxMinPower, txMaxPower, SNRThreshold, noiseFig, offset):
    pathLoss = abs(txPower) - abs(rxPower)
    algPower = (abs(rxMinPower) - abs(pathLoss))*(1+offset)
    print("Algorithm calculated power: %f" %(algPower))
    if algPower - pathLoss - noiseFig < SNRThreshold:
        algPower = SNRThreshold + noiseFig + pathLoss
    return min(txMaxPower, algPower)

def NetworkTPCAlgorithm(rssi, txpower, offset):
    1

def ltePowerControl():
    1

class Channel(object):
    def __init__(self, snr=0, shadowingStd=1):
        self.noisePower = snr
        self.exponent = 2
        self.refdist=1000 # reference distance from the transmitter in meters
        self.ref = 20*np.log10(4*np.pi*self.refdist*CENTER_FREQ/3e8)
        self.shadowingStd = shadowingStd

    def transportMessage(self, message, tx, rx, verbose=False):
        dataLen = len(message.payload)
        noise = np.random.normal(0,1, dataLen)
        dist = np.hypot(tx.x-rx.x, tx.y-rx.y)
        shadowing =  np.random.normal(0,self.shadowingStd)
        distComponent = 10*self.exponent*np.log10(dist/self.refdist)
        pathLoss = self.ref + distComponent + shadowing
        message.power -= pathLoss
        rx.receiveMessage(message)
        if verbose is True:
            print("Path Loss Reference: %f" % self.ref)
            print("shadowing: %f" % (shadowing))
            print("Distance: %f" % dist)
            print("Distance component: %f" % (distComponent))
            print("Path Loss: %f" % pathLoss)
            print("Message Power: %f" % (message.power))



class Battery(int):
    def __init__(self,voltage=3,drawncurrent=200):
        self.charge=voltage*drawncurrent*3.6

    def sendMessage(self, spent, length):
        self.charge -= 1e-6*length

    def receiveMessage(self, spent, length):
        self.charge -= 1e-6*length

    def stayAwake(self, spent, time):
        self.charge -= 1e-6*time

    def stayAsleep(self, spent, time):
        self.charge -= 1e-6*time

class Message(str):
    def __new__(cls, *args, **kw):
        return str.__new__(cls, *args, **kw)

    def __init__(self, payload='', Id=None, power=0):#, tx, rx):
        str.__init__(payload)
        self.header = None
        self.payload = payload
        self.status = None
        self.id = Id
        self.power = power
        #self.transmitter = tx
        #self.receiver = rx

    def length(self):
        return len(self.payload)

    def loremIpsum(self,length):
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
        'cursus ex convallis. In non mollis nisi, quis ullamcorper nunc. Sed '+\
        'elementum est vel nisi dapibus posuere.'

        self.payload = lorem[:length]

    def setHeader(self, header):
        self.header = header
        

def ofdm_tx(x, nfft, nsc, cp_length):
    """ OFDM Transmit signal generation """

    #nfft = float(nfft)
    #nsc = float(nsc)
    #cp_length = float(cp_length)
    ofdm_tx_signal = np.array([])

    for i in range(0, np.shape(x)[0]):
        symbols = x[i,:]
        ofdm_sym_freq = np.zeros(nfft, dtype=complex)
        ofdm_sym_freq[1:int(nsc / 2)+1] = symbols[int(nsc / 2):]
        ofdm_sym_freq[-int(nsc / 2):] = symbols[0:int(nsc / 2)]
        ofdm_sym_time = np.fft.ifft(ofdm_sym_freq)
        cp = ofdm_sym_time[-cp_length:]
        ofdm_tx_signal = np.concatenate((ofdm_tx_signal, cp, ofdm_sym_time))

    return ofdm_tx_signal

def ofdm_rx(y, nfft, nsc, cp_length):
    """ OFDM Receive Signal Processing """

    num_ofdm_symbols = int(len(y) / (nfft + cp_length))
    x_hat = np.zeros([nsc, num_ofdm_symbols], dtype=complex)

    for i in range(0, num_ofdm_symbols):
        ofdm_symbol = y[i * nfft + (i + 1) * cp_length:(i + 1) * (nfft + cp_length)]
        symbols_freq = np.fft.fft(ofdm_symbol)
        x_hat[:, i] = np.concatenate((symbols_freq[int(-nsc / 2):], symbols_freq[1:int(nsc / 2) + 1]))

    return x_hat


class Sensor(object):
    def __init__(self,scenario, gain=0, Id=1):
        self.scenario = scenario
        self.x=scenario.radius
        self.y=scenario.radius
        self.txPower=10
        self.period = 1 #1 hour
        self.lifecycle = {
            'awake':10, #seconds
            'sleep':10*60 - 10, #seconds
            'alive':True
            }

        self.id = Id
        self.battery = Battery()

        self.antennaGain = 0 #antenna gain in dB
        self.power = 23 #in dBm

        self.TPCOffset = 1
        self.cache = []


        while self.x**2 + self.y**2 > (self.scenario.radius**2):
            self.x = np.random.uniform(-self.scenario.radius, self.scenario.radius)
            self.y = np.random.uniform(-self.scenario.radius, self.scenario.radius)

    def setMessagePeriod(self, period):  
        self.period = period
        self.scenario.process(self.transmitMessage())

    def transmitMessage(self):
        while True:
            yield self.scenario.timeout(self.period)
            msg = Message()
            msg.loremIpsum(8)
            power = sensorTPCAlgorithm(38,-138+np.random.normal(0,10), self.scenario.network.sensibility, self.power, self.scenario.network.SNRThreshold, self.scenario.noiseFigure, self.TPCOffset)
            msg.power = self.antennaGain + power
            self.battery.sendMessage(None,msg.length())
            self.scenario.sendUserMessage(msg, self)       


    def receiveMessage(self, message):
        self.battery.receiveMessage()
        print(message.payload)

    

class Network(object):
    def __init__(self, power=30):
        self.txPower = power
        self.bandwith = 400e6 #hertz
        self.centerFreq = 700e6 #hertz
        self.modulation = 4
        self.nsubcarriers = 16

        self.sensibility = -110 #dBm
        self.modulator = mod.PSKModem(self.modulation)

        self.x = 0
        self.y = 0

        self.antennaGain = 8
        self.users = []
        self.SNRThreshold = 20


    def transmitMessage(self):
        while True:
            yield self.scenario.timeout(self.period)
            msg = Message()
            msg.loremIpsum(8)
            msg.power = self.power + self.antennaGain
            self.battery.sendMessage(None,msg.length())
            self.scenario.sendNetworkMessage(msg, self)       


    def receiveMessage(self, message):
        self.battery.receiveMessage()
        print(message.payload)

    def receiveMessage(self, message):
        #print(message)
        if message.power + self.antennaGain >= self.sensibility:
            print(message.payload)
        else:
            print("Unsuficient transmited power %d (received) x %d (sensibility)" % (message.power, self.sensibility))
        

class Scenario(sp.Environment):
    def __init__(self, radius=50000):#radius im meter
        sp.Environment.__init__(self)
        self.radius = radius
        self.network = Network()
        self.sensors = []
        self.channel = Channel()
        self.noiseFigure = 10*np.log10(BANDWIDTH*1.38e-23*290)
    
    def turnOnSensor(self, turnOnTime, period, Id):
        yield self.timeout(turnOnTime)
        self.sensors[Id].setMessagePeriod(period)


    def spreadsensors(self, nsensors):
        check = []
        while len(check) < nsensors:
            sensor = Sensor(self,0,len(check))
            if check.count([sensor.x, sensor.y]) == 0:
                self.sensors.append(sensor)
                check.append([sensor.x, sensor.y])
                offset = np.random.poisson(30)
                self.process(self.turnOnSensor(offset, 1800,self.sensors[-1].id))
        self.network.users = self.sensors


    def sendUserMessage(self, message, sensor):
        print(self.now)
        self.channel.transportMessage(message, sensor, self.network, True)

    def sendNetworkMessage(self, message, sensor):
        print(self.now)
        self.channel.transportMessage(message, self.network, sensor, True)

        


if __name__=="__main__":
    env = Scenario()
    env.spreadsensors(10)
    env.run(until=SIMULATION_TIME)
