#! /usr/bin/env python3

import matplotlib.pyplot as plt
import scipy as sc
from scipy import stats
import os
import sys
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--time',action='store_true')
parser.add_argument('--loss',action='store_true')
parser.add_argument('--snr',action='store_true')
parser.add_argument('--std',action='store_true')
parser.add_argument('--save',action='store_true')
parser.add_argument('--error',action='store_true')

args = parser.parse_args()
timeOption = args.time
lossOption = args.loss
snrOption = args.snr
stdOption = args.std
saveOption = args.save
errorOption = args.error


algorithm = ['open','notpc','closed','lte']
mkr=['+','^', 'o','s']
snr = [str(i*2) for i in range(11)]
stdDev = [str(i*2 + 1) for i in range(5)]
cl = ['blue', 'red', 'green', 'orange', 'hotpink', 'black']

runs = range(50)

directory = 'results/'

timeAlive = []
stdTime = []
packetLoss = []
stdLoss = []

for alg in algorithm:
    filename = directory + alg + '/out/'
    counter = 0
    timeAlive.append([])
    stdTime.append([])
    packetLoss.append([])
    stdLoss.append([])
    for s in snr:
        timeAlive[-1].append([])
        stdTime[-1].append([])
        packetLoss[-1].append([])
        stdLoss[-1].append([])
        for d in stdDev:
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
print(len(stdTime), len(stdTime[0]), len(stdTime[0][0]), len(stdTime[0][0][0]))
print(stdTime[2][10][0][0] + timeAlive[2][10][0], timeAlive[2][10][0], stdTime[2][10][0][1] + timeAlive[2][10][0])

if timeOption:
    plt.ylabel('Average Network Alive Time [%]')
    if snrOption:
        for i in range(len(algorithm)):
            for j in range(len(stdDev)):
                if j == 1 or j == 3:
                    continue
                plot = []
                errorbar = []
                for k in range(len(snr)):
                    plot.append(timeAlive[i][k][j])
                    errorbar.append(stdTime[i][k][j])
                plt.xlabel('SNR Threshold [dB]')
                plt.plot(snr,plot, label=algorithm[i]+',$\sigma$='+stdDev[j], marker=mkr[i], color=cl[j])
                #print(sc.reshape(errorbar,(2,len(errorbar))))
                #print(sc.transpose(errorbar,(1,0)))
                if errorOption:
                    plt.errorbar(snr,plot, color=cl[j], yerr=sc.transpose(errorbar,(1,0)))#sc.reshape(errorbar,(2,len(errorbar))))
                if saveOption:
                    figname = 'time-snr.eps'

    elif stdOption:
        timeAlive = sc.array(timeAlive)
        temp = []
        for i in range(len(algorithm)):
            temp.append(timeAlive[i].transpose())
        timeAlive = temp
        #print(len(timeAlive), len(timeAlive[0]), len(timeAlive[0][0]))
        stdTime = sc.array(stdTime)
        temp = []
        for i in range(len(algorithm)):
            temp.append(stdTime[i].transpose((1,0,2)))
        stdTime = temp

        for i in range(len(algorithm)):
            for j in range(len(snr)):
                if j==0 or j==5 or j==10:
                    plot = []
                    errorbar = []
                    for k in range(len(stdDev)):
                        plot.append(timeAlive[i][k][j])
                        errorbar.append(stdTime[i][k][j])
                    plt.xlabel('Shadowing Standard Deviation')
                    plt.plot(stdDev,plot, label=algorithm[i]+',snr='+snr[j], marker=mkr[i], color=cl[int(j/2)])
                    if errorOption:
                        plt.errorbar(stdDev,plot, color=cl[int(j/2)], yerr=sc.transpose(errorbar,(1,0)))#sc.reshape(errorbar,(2,len(errorbar))))
                    if saveOption:
                        figname = 'time-stddev.eps'
                else:
                    continue




elif lossOption:
    plt.ylabel('Packet Loss [%]')
    if snrOption:
        for i in range(len(algorithm)):
            for j in range(len(stdDev)):
                if j == 1 or j == 3:
                    continue
                plot = []
                errorbar = []
                for k in range(len(snr)):
                    plot.append(packetLoss[i][k][j])
                    errorbar.append(stdLoss[i][k][j])
                plt.xlabel('SNR Threshold [dB]')
                plt.plot(snr,plot, label=algorithm[i]+',$\sigma$='+stdDev[j], marker=mkr[i], color=cl[j])
                if errorOption:
                    plt.errorbar(snr,plot, color=cl[j], yerr=sc.transpose(errorbar,(1,0)))#sc.reshape(errorbar,(2,len(errorbar))))
                if saveOption:
                    figname = 'packetloss-snr.eps'
    elif stdOption:
        packetLoss = sc.array(packetLoss)
        temp = []
        for i in range(len(algorithm)):
            temp.append(packetLoss[i].transpose())
        packetLoss = temp

        stdLoss = sc.array(stdLoss)
        temp = []
        for i in range(len(algorithm)):
            temp.append(stdLoss[i].transpose((1,0,2)))
        stdLoss = temp

        for i in range(len(algorithm)):
            for j in range(len(snr)):
                if j==0 or j==5 or j==10:
                    plot = []
                    errorbar = []
                    for k in range(len(stdDev)):
                        plot.append(packetLoss[i][k][j])
                        errorbar.append(stdLoss[i][k][j])
                    plt.xlabel('Shadowing Standard Deviation')
                    plt.plot(stdDev,plot, label=algorithm[i]+',snr='+snr[j], marker=mkr[i], color=cl[int(j/2)])
                    if errorOption:
                        plt.errorbar(stdDev,plot, color=cl[int(j/2)], yerr=sc.transpose(errorbar,(1,0)))#sc.reshape(errorbar,(2,len(errorbar))))
                    if saveOption:
                        figname = 'packetloss-stddev.eps'
                else:
                    continue


plt.legend(ncol=4, bbox_to_anchor=(1.1,-0.15))
plt.tight_layout()
plt.grid()
if saveOption:
    plt.savefig(figname,metadata='eps')

plt.show()
