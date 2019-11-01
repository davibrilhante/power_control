#! /bin/bash
SNR=`seq 0 2 20`
DEV=`seq 1 1 10`
OFFSET=`seq 0.1 0.1 1`
ONOFF=1
SEED=`seq 1 100`
RUN=30
DURATION=(1 60 600 900 1800 3600)
YEARS=1

for s in ${SNR[@]}
	do
	for d in ${DEV[@]}
	do
		echo -e "\nArguments = ${DURATION[2]} 30 $s 0.1 $ONOFF $d 1 \$(Process)\nQueue $RUN\n\n" >> submit.sub;
	done
done
