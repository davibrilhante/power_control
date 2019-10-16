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

CENTER_FREQ=700e3
SIMULATION_TIME=st.seconds(24*3600)


'''
class Transmitter(gr.hier_block2):
    def __init__(self, channelCoding, codingRate, blockLen):
        self.coding = channelCoding
        self.rate = codingRate
        self.blockLen = blockLen
        gr.hier_block2.__init__(self, "HierBlock",gr.io_signature(1, 1, gr.sizeof_char),
                gr.io_signature(1, 2, gr.sizeof_gr_complex))

        ofdm = phy.ofdm_tx()
        scrambler = 
        encoder = fec.encoder()
        crc = 
        self.connect(self, block1)
        self.connect(blockn, self)
'''

def powerControlAlgorithm(rssi, txpower, offset):
    1

def ltePowerControl():
    1

class Channel: 
    def __init__(self, Type='rayleigh', freq=700e6, bw=400e6):
        self.pathLoss = 0
        self.bandwidth = bw
        self.centerFreq = freq
        self.type = Type
        self.stdDev = 1



    def transportMessage(self, message, Input, Output):
        '''
        obj1 = Sensor(None)
        obj2 = Network()
        if type(Input)==type(obj1): dist = np.sqrt(Input.x**2 + Input.y**2)
        elif type(Input)==type(obj2): dist = np.sqrt(Output.x**2 + Output.y**2)
        '''
        if self.type == 'no-fading':
            self.channel = ch.SISOFlatChannel(self.stdDev, (1j,0))
        elif self.type =='rayleigh':
            self.channel = ch.SISOFlatChannel(self.stdDev, (1j,0))

        received = self.channel.propagate(message)
            
        Output.receiveMessage(received)
            
        


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

    def __init__(self, payload='', Id=None):#, tx, rx):
        str.__init__(payload)
        self.payload = payload
        self.status = None
        self.id = Id
        #self.transmitter = tx
        #self.receiver = rx

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
        self.modulation = 4
        self.nsubcarriers = 16
        self.data = 0


        while self.x**2 + self.y**2 > self.scenario.radius:
            self.x = np.random.uniform(-self.scenario.radius, self.scenario.radius)
            self.y = np.random.uniform(-self.scenario.radius, self.scenario.radius)

    def setMessagePeriod(self, period):  
        self.period = period
        self.scenario.process(self.transmitMessage())

    def transmitMessage(self):
        msg = Message()
        msg.loremIpsum(8)
        modulator = mod.PSKModem(self.modulation)
        a = [bin(ord(x))[2:].zfill(8) for x in msg.payload]
        binary = [int(j) for i in a for j in i]
        constellation = modulator.modulate(binary)
        symbol = np.array([constellation[i*self.nsubcarriers:(i+1)*self.nsubcarriers] for i in range(int(len(constellation)/self.nsubcarriers))]) #[i for i in constellation]
        signal = ofdm_tx(symbol, 64, self.nsubcarriers, 0)
        while True:
            yield self.scenario.timeout(self.period)
            self.scenario.sendThroughChannel(signal, self)       


    def receiveMessage(self, message):
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

    def transmitMessage(self):
        msg = Message()
        msg.loremIpsum(12)
        while True:
            yield self.scenario.timeout(self.period)
            self.scenario.sendThroughChannel(msg, self)       

    def receiveMessage(self, message):
        #print(message)
        symbols = ofdm_rx(message,64,self.nsubcarriers,0)
        symbols = [j for i in symbols for j in i]
        bits = self.modulator.demodulate(symbols,'hard')
        message = []
        for i in range(int(len(bits)/8)):
            temp = []
            for j in range(8):
                temp.append(bits[j+(i*8)]*2**j)
            message.append(chr(sum(temp)))
        print()
        

class Scenario(sp.Environment):
    def __init__(self, radius=1000):
        sp.Environment.__init__(self)
        self.radius = radius
        self.network = Network()
        self.sensors = []
        self.channel = Channel()
    
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


    def sendThroughChannel(self, message, sensor):
        print(self.now)
        self.channel.transportMessage(message, sensor, self.network)
        


if __name__=="__main__":
    env = Scenario()
    env.spreadsensors(10)
    env.run(until=SIMULATION_TIME)
