#!/bin/bash -e

if [ $# -lt 3 ]
then
    echo usage: $0 [OUTPUT_PATH] [THREADS] [b37/hg38/...]
    exit 1
fi


output=$1
threads=$2

case "$3" in
    "b37")
        input_ref_fasta=""
        gtf_path="/home/jun9485/workingDir/b37/gatk-legacy-bundles/b37/GRch37_GTF/Homo_sapiens.GRCh37.87.gtf"
    ;;
    "hg38")
        input_ref_fasta="/data/refGenome/hg38/GDC/GRCh38.d1.vd1.fa"
        gtf_path="/data/refGenome/GRch38_GTF/gencode.v38.primary_assembly.annotation.gtf"
    ;;
    *)
        echo "해당 파일의 GTF파일 없음. GTF파일의 경로를 확인하시오."
        exit 1
    ;;
esac

source activate star
STAR\
    --runThreadN $threads\
    --runMode genomeGenerate\
    --genomeDir $output\
    --genomeFastaFiles $input_ref_fasta\
    --sjdbGTFfile $gtf_path\
    #--sjdbOverhang 100 << 디폴트 옵션. sample report에 보면 101이라고 나와있음
source deactivate

