#!/bin/bash -e

if [ $# -lt 3 ]
then
    echo usage: $0 [bamFile] [gtfFile] [output_dir]
    exit 1
fi

bam_file=$1
gtf_file=$2
output_path=$3

 
htseq-count\
    -i gene_name \
    -s no \
    -f bam \
    $bam_file $gtf_file > $output_path

sleep 10s