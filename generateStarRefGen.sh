#!/bin/bash -e

if [ $# -lt 4 ]
then
    echo usage: $0 [INPUT_FASTA_FILE] [OUTPUT_PATH] [THREADS] [b37/hg38/...]
    exit 1
fi

input=$1
output=$2
threads=$3

case "$4" in
    "b37")
        gtf_path="/home/jun9485/workingDir/b37/gatk-legacy-bundles/b37/GRch37_GTF/Homo_sapiens.GRCh37.87.gtf"
    ;;
    "hg38")
        gtf_path="hg38_GTF_path"
    ;;
    *)
        echo "해당 파일의 GTF파일 없음. GTF파일의 경로를 확인하시오."
        exit 1
    ;;
esac

source activate star
star\
    --runThreadN $threads\
    --runMode genomeGenerate\
    --genomeDir $output\
    --genomeFastaFiles $input\
    --sjdbGTFfile $gtf_path\
    #--sjdbOverhang 99 # Ideally, readLength-1
source deactivate

