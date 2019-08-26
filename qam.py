import numpy as np
from commpy import modulation as modem
from matplotlib import pyplot as plt

class Qam:
    def __init__(self, modulation="4_QAM"):
        self.modulation = modulation
        if modulation == "4_QAM":
            self.bitsPerBaud = 2
            self.nSymbols = 4
        elif modulation == "8_QAM":
            self.bitsPerBaud = 3
            self.nSymbols = 8
        elif modulation == "16_QAM":
            self.bitsPerBaud = 4
            self.nSymbols = 16
        elif modulation == "64_QAM":
            self.bitsPerBaud = 6
            self.nSymbols = 64
        #self.baudRate = baudRate
        self.modem = modem.QAMModem(self.nSymbols)

    def modulate(self, data):
        return self.modem.modulate(data)

    def demodulate(self, data):
        return self.modem.demodulate(data)

    def plotConstellation(self):
        array = [] 
        for i in range(self.nSymbols):
            temp = [int(j) for j in list(bin(i)[2:])]
            if len(temp) < self.bitsPerBaud:
                temp = [0 for j in range(self.bitsPerBaud - len(temp))] + temp
            array += temp
        print(array)
        constellation = [self.modem.modulate(array), [array[i*self.bitsPerBaud:(i+1)*self.bitsPerBaud] for i in range(self.nSymbols)]]

        data = [(i.real,i.imag, t)
               for i,t in zip(constellation[0], constellation[1])]
        I,Q,T = zip(*data)
        print(T)
        plt.scatter(I, Q)
        for x,y,t in data:
            plt.annotate(t,(x+.08,y-.03), ha='right', va='top')
        plt.xlabel("I")
        plt.ylabel("Q")
        plt.xlim(min(I)-1, max(I)+1)
        plt.ylim(min(Q)-1, max(Q)+1)
        plt.grid(True)
        plt.show()
