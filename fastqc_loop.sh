#!/bin/bash -e

if [ $# -lt 2 ]
then
    echo 편집기로 inputdir의 경로를 지정해 줘야함
    echo usage: $0 [OUTPUT_PATH] [THREADS]
    exit 1
fi

output_dir=$1
threads=$2


source activate star
for path in ~/WES/HN00144124/Te*; do
    fastqc\
    -o $output_dir\
    -t $threads\
    --noextract $path
done
source deactivate
