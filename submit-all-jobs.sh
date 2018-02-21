#!/usr/bin/bash
JOBS=( "open_telemac/submit_testcase1"\
	"open_telemac/submit_testcase2"\
	"open_telemac/submit_testcase3"\
	"mic-jobs/4.01-overview-nbody/submit-job.sh"\
	"mic-jobs/4.02-vectorization-data-structures-coulomb/submit-job.sh"\
	"mic-jobs/4.03-vectorization-tuning-lu-decomposition/submit-job.sh"\
	"mic-jobs/4.04-threading-misc-histogram/submit-job.sh"\
	"mic-jobs/4.05-threading-insufficient-parallelism-sweep/submit-job.sh"\
	"mic-jobs/4.06-threading-scheduling-jacobi/submit-job.sh"\
	"mic-jobs/4.07-threading-affinity/submit-job.sh"\
	"mic-jobs/4.08-memory-tiling-matrix_x_vector/submit-job.sh"\
	"qe/submit-job.sh"\
	"vast/si/submit-job.sh")

NJOBS=( 2 14 28 38 38 30 20 10 4 4 4 4 2 2 )
RANGEJOBS=13

for i in {0..13}
do
	
	N=${NJOBS[${i}]}
	echo "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
	for (( j=0; j < $N; j++))
	do
		echo "-------------------------------------------"
		random_num=$RANDOM
		let "	random_num %= $RANGEJOBS"
		echo "	Randomize job submission: $random_num"
		
		echo "	Submitting job $random_num"
		echo "	Num of jobs = ${NJOBS[${i}]}"
		qsub /home/ctminh/pbs/jobs/${JOBS[${random_num}]}
		echo "-------------------------------------------"
	done
	
	rand_seconds=$(shuf -i 30-60 -n 1)
	echo "Randomize delay for submitting jobs: $rand_seconds"
	sleep $rand_seconds
	echo "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
done

echo "End of submission"
	
	