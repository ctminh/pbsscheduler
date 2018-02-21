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

#	Formula to calculate due_date:
#																					Exec_Time	Due_date	F
# 0 - submit_testcase1: 03:30:00	(1 chunck: 24CPU)								210s x 3	420			630
# 1 - submit_testcase2: 04:00:00	(1 chunck: 16CPU)								240s x 3	480			720
# 2 - submit_testcase3: 03:00:00	(2 chunck: 24CPU)								180s x 3	360			540
# 3 - 4.01-overview-nbody: 00:15:00	(1 chunck: 12CPU)								15s	 + 60	60			75
# 4 - 4.02-vectorization-data-structures-coulomb: 00:10:00		(1 chunck: 12CPU)	10s	 + 120	120			130
# 5 - 4.03-vectorization-tuning-lu-decomposition: 00:05:00		(1 chunck: 24CPU)	5s	 + 45	45			50
# 6 - 4.04-threading-misc-histogram: 				00:10:00	(1 chunck: 32CPU)	10s	 + 60	60			70
# 7 - 4.05-threading-insufficient-parallelism-sweep: 00:10:00	(1 chunck: 8CPU)	10s	 + 30	30			40
# 8 - 4.06-threading-scheduling-jacobi: 			01:00:00	(1 chunck: 16CPU)	60s	 + 150	150			210
# 9 - 4.07-threading-affinity:						00:30:00	(1 chunck: 16CPU)	30s	 + 120	120			150
# 10 - 4.08-memory-tiling-matrix_x_vector: 			00:05:00	(1 chunck: 16CPU)	5s	 + 30	30			35
# 11 - qe: 20:00:00		(1 chucnk: 32 CPU - 1 mic)									1200s x 4	3600		4800
# 12 - vast: 10:00:00	(1 chunck: 48CPU)											600s  x 3	1200		1800
	
#qsub /home/ctminh/pbs/jobs/${JOBS[0]}
#qsub /home/ctminh/pbs/jobs/${JOBS[0]}
#qsub /home/ctminh/pbs/jobs/${JOBS[2]}
#qsub /home/ctminh/pbs/jobs/${JOBS[11]}
#sub /home/ctminh/pbs/jobs/${JOBS[11]}
#qsub /home/ctminh/pbs/jobs/${JOBS[6]}
#qsub /home/ctminh/pbs/jobs/${JOBS[6]}
#qsub /home/ctminh/pbs/jobs/${JOBS[6]}
#for i in {1401..1626}
#do
#	qdel $i
#done
