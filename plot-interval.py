#! /usr/bin/env python3

import matplotlib.pyplot as plt
import scipy as sc
from scipy import stats
import os
import sys
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--time',action='store_true', help='Choose the y axis of the plot. Use instead of --loss')
parser.add_argument('--loss',action='store_true',  help='Choose the y axis of the plot. Use instead of --time')
parser.add_argument('--snr',action='store_true',  help='Choose the auxiliar metric. Use instead of --std')
parser.add_argument('--std',action='store_true', help='Choose the auxiliar metric. Use instead of --snr')
parser.add_argument('--save',action='store_true', help='saves the plot')
parser.add_argument('--error',action='store_true', help='enable error bars')

args = parser.parse_args()
timeOption = args.time
lossOption = args.loss
snrOption = args.snr
stdOption = args.std
saveOption = args.save
errorOption = args.error


algorithm = ['open','closed']
mkr=['+','^', 'o','s']
snr = [str(i*10) for i in range(3)]
stdDev = [str(1 + i*4) for i in range(3)]
offset = [str(round(2*i*0.1 + 0.1,1)) for i in range(5)] + ['1']
cl = ['blue', 'red', 'green', 'orange', 'hotpink', 'black']

runs = range(50)

directory = 'interval/'

timeAlive = []
stdTime = []
packetLoss = []
stdLoss = []

for alg in algorithm:
    filename = directory + alg + '/out/'
    timeAlive.append([])
    stdTime.append([])
    packetLoss.append([])
    stdLoss.append([])
    if snrOption:
        for s in snr:
            timeAlive[-1].append([])
            stdTime[-1].append([])
            packetLoss[-1].append([])
            stdLoss[-1].append([])
            for i in range(len(stdDev)):
                counter = 300 + 900*i
                for d in offset:
                    temp1 = []
                    temp2 = []
                    for r in runs:
                        f = open(filename+str(counter))
                        lines = f.readlines()
                        temp1.append(float(lines[0].strip('\n'))*100/365)
                        temp2.append(float(lines[1].strip('\n'))*100)

                        counter += 1
                    timeAlive[-1][-1].append(sc.mean(temp1))
                    stdTime[-1][-1].append([timeAlive[-1][-1][-1] - i for i in stats.norm.interval(0.9, loc=timeAlive[-1][-1][-1], scale=sc.std(temp1))])
                    packetLoss[-1][-1].append(sc.mean(temp2))
                    stdLoss[-1][-1].append([packetLoss[-1][-1][-1] - i for i in stats.norm.interval(0.9, loc=packetLoss[-1][-1][-1], scale=sc.std(temp2))])

    if stdOption:
        counter = 900
        for s in stdDev:
            timeAlive[-1].append([])
            stdTime[-1].append([])
            packetLoss[-1].append([])
            stdLoss[-1].append([])
            for d in offset:
                temp1 = []
                temp2 = []
                for r in runs:
                    f = open(filename+str(counter))
                    lines = f.readlines()
                    temp1.append(float(lines[0].strip('\n'))*100/365)
                    temp2.append(float(lines[1].strip('\n'))*100)

                    counter += 1
                timeAlive[-1][-1].append(sc.mean(temp1))
                stdTime[-1][-1].append([timeAlive[-1][-1][-1] - i for i in stats.norm.interval(0.9, loc=timeAlive[-1][-1][-1], scale=sc.std(temp1))])
                packetLoss[-1][-1].append(sc.mean(temp2))
                stdLoss[-1][-1].append([packetLoss[-1][-1][-1] - i for i in stats.norm.interval(0.9, loc=packetLoss[-1][-1][-1], scale=sc.std(temp2))])


if timeOption:
    plt.ylabel('Average Network Alive Time [%]')
    if snrOption:
        for i in range(len(algorithm)):
            for j in range(len(snr)):
                plot = []
                errorbar = []
                for k in range(len(offset)):
                    plot.append(timeAlive[i][j][k])
                    errorbar.append(stdTime[i][j][k])
                print(plot)
                plt.xlabel('TPC Offset')
                plt.plot(offset,plot, label=algorithm[i]+',snr='+snr[j], marker=mkr[i], color=cl[j])
                if errorOption:
                    plt.errorbar(offset,plot, color=cl[j], yerr=sc.reshape(errorbar,(2,len(errorbar))))
                if saveOption:
                    figname = 'offset-time-snr.eps'

    elif stdOption:
        for i in range(len(algorithm)):
            for j in range(len(stdDev)):
                plot = []
                errorbar = []
                for k in range(len(offset)):
                    plot.append(timeAlive[i][j][k])
                    errorbar.append(stdTime[i][j][k])
                print(plot)
                plt.xlabel('TPC Offset')
                plt.plot(offset,plot, label=algorithm[i]+',$\sigma$='+stdDev[j], marker=mkr[i], color=cl[j])
                if errorOption:
                    plt.errorbar(offset,plot, color=cl[j], yerr=sc.reshape(errorbar,(2,len(errorbar))))
                if saveOption:
                    figname = 'offset-time-stddev.eps'




elif lossOption:
    plt.ylabel('Packet Loss [%]')
    if snrOption:
        for i in range(len(algorithm)):
            for j in range(len(snr)):
                plot = []
                errorbar = []
                for k in range(len(offset)):
                    plot.append(packetLoss[i][j][k])
                    errorbar.append(stdLoss[i][j][k])
                print(plot)
                plt.xlabel('TPC Offset')
                plt.plot(offset,plot, label=algorithm[i]+',snr='+snr[j], marker=mkr[i], color=cl[j])
                if errorOption:
                    plt.errorbar(offset,plot, color=cl[j], yerr=sc.reshape(errorbar,(2,len(errorbar))))
                if saveOption:
                    figname = 'offset-packetloss-snr.eps'
    elif stdOption:
        for i in range(len(algorithm)):
            for j in range(len(stdDev)):
                plot = []
                errorbar = []
                for k in range(len(offset)):
                    plot.append(packetLoss[i][j][k])
                    errorbar.append(stdLoss[i][j][k])
                print(plot)
                plt.xlabel('TPC Offset')
                plt.plot(offset,plot, label=algorithm[i]+',$\sigma$='+stdDev[j], marker=mkr[i], color=cl[j])
                if errorOption:
                    plt.errorbar(offset,plot, color=cl[j], yerr=sc.reshape(errorbar,(2,len(errorbar))))
                if saveOption:
                    figname = 'offset-packetloss-stddev.eps'


plt.legend(ncol=4, bbox_to_anchor=(0.85,-0.15))
plt.tight_layout()
plt.grid()
if saveOption:
    plt.savefig(figname,metadata='eps')

plt.show()
