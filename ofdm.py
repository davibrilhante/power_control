import numpy as np
from qam import Qam
def naive_DFT(x):
    N = np.size(x)
    X = np.zeros((N,),dtype=np.complex128)
    for m in range(0,N):    
        for n in range(0,N): 
            X[m] += x[n]*np.exp(-np.pi*2j*m*n/N)
    return X

def naive_IDFT(x):
    N = np.size(x)
    X = np.zeros((N,),dtype=np.complex128)
    for m in range(0,N):
        for n in range(0,N): 
            X[m] += x[n]*np.exp(np.pi*2j*m*n/N)
    return X/N

numberSubcarriers = 64
cyclicPrefix = numberSubcarriers/4
numberPilots = 8
pilotValue = 3+3j


carriers = np.arange(numberSubcarriers)

pilotCarriers = carriers[::numberSubcarriers//numberPilots]
pilotCarriers = np.hstack([pilotCarriers, np.array([carriers[-1]])])
print(pilotCarriers)

dataCarriers = np.delete(carriers,pilotCarriers)
print(dataCarriers)

bitsSymbol = 4 #16 qam...implementar modulacoes
bitsOfdmSymbol = bitsSymbol*len(dataCarriers)
"""
x = np.random.rand(1024,)
X = naive_DFT(x)
Y = naive_IDFT(X)
print(x)
print(X)
print(Y)
"""
qam2 = Qam("16_QAM")
qam2.plotConstellation()
