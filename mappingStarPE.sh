#!/bin/bash -e

if [ $# -lt 5 ]
then
    echo usage: $0 [fastq1] [fastq2] [threads] [refGenomeDir] [/path/to/output/dir/prefix]
    exit 1
fi

 
fastq1=$1
fastq2=$2
threads=$3
star_genome=$4
output_prefix=$5

# RG="@RG\tID:$output_prefix\tPL:illumina\tPU:ex\tLB:$output_prefix\tSM:$output_prefix"
 
source activate star
STAR\
    --genomeDir $star_genome\
    --readFilesIn $fastq1 $fastq2\
    --runThreadN $threads\
    --outFileNamePrefix $output_prefix\
    --outSAMtype BAM SortedByCoordinate\
    --outSAMattributes NH HI AS NM MD \
    --outFilterType BySJout \
    --outFilterMultimapNmax 20 \
    --outFilterMismatchNmax 999 \
    --outFilterMismatchNoverReadLmax 0.04 \
    --alignIntronMin 20 \
    --alignIntronMax 1000000 \
    --alignMatesGapMax 1000000 \
    --alignSJoverhangMin 8 \
    --alignSJDBoverhangMin 1 \
    --sjdbScore 1 \
    --outSAMstrandField intronMotif\
    --limitBAMsortRAM 88170903896\
    --quantMode TranscriptomeSAM\
    --readFilesCommand zcat
 
conda deactivate
