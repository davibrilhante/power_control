#! /bin/bash

touch submit


SNR=`seq 0 2 20`
DEV=`seq 1 2 10`
OFFSET=0.1 #`seq 0.1 0.2 1`
ONOFF=1
SEED=`seq 1 50`
#RUN=30
DURATION=(1 60 600 900 1800 3600)
YEARS=1

for s in ${SNR[@]}
	do
	for d in ${DEV[@]}
	do
		for x in ${SEED[@]}
		do
			#echo -e "\nArguments = ${DURATION[2]} 30 $s 0.1 $ONOFF $d 1 \$(Process)\nQueue $RUN\n\n" >> submit;
			touch results/output_$1_$s_$d_$x
			echo -e "python3 $1 ${DURATION[2]} 30 $s 0.1 $ONOFF $d 1 $x >> results/output_$1_$s_$d_$x" >> submit;
		done
	done
done

parallel < submit
