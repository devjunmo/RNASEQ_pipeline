import subprocess as sp
import glob
import natsort
import time
from time import sleep
import os

# script형태의 python 파일
# 사용시 hyper parameters에 해당하는 부분 유동적으로 수정
# paired end 기준으로 돌아감 

####################### hyper parameters ########################################
sample_group_name = 'RNASEQ_2samples'

is_making_input_list = True

REF_GENOME_DIR = r'/data_244/refGenome/star_genome_hg38_GDC'
GTF_path = r'/data_244/refGenome/GRch38_GTF/gencode.v38.primary_assembly.annotation.gtf'
# REF_GENOME_DIR = r'/home/jun9485/data/star_genome_b37'
# GTF_path = r'/home/jun9485/data/GRch37_GTF/Homo_sapiens.GRCh37.87.gtf'

seq_type = "RNA"

# mode : pp, qc
run_mode = 'pp'



INPUT_DIR = r'/data_244/stemcell/RNA/RNAseq_211229_2samples_BCell/'   # 이 디렉토리에 계속 생성시킬것
RAW_READS = r'*.fastq.gz'

SRC_DIR = r'/data_244/src/RNA/RNASEQ_pipeline/'

# QC
qc_output_dir_name = 'QC_results'
qc_threads = 1

qc_output_dir = os.path.join(INPUT_DIR, qc_output_dir_name)

if os.path.isdir(qc_output_dir) is False:
    os.mkdir(qc_output_dir)


## pbs config
pbs_N = "RNAseq.10"
pbs_o = INPUT_DIR + r"qsub_log/"
pbs_j = "oe"
pbs_l_core = 5


if os.path.isdir(pbs_o) is False:
    os.mkdir(pbs_o)

#################################################################################

def mk_init_file_list(_input_dir, _raw_read_form, group_name): # fastq파일의 부재로 중간지점 스타트 불가능한 문제 해결목적
    _input_path_list = glob.glob(_input_dir + _raw_read_form)
    _input_path_list = natsort.natsorted(_input_path_list)
    _output_path = _input_dir + sample_group_name + '.txt'
    
    f = open(f'{_output_path}', mode='w')
    for i in range(len(_input_path_list)):
        data = f'{_input_path_list[i]}\n'
        f.write(data)
    f.close



if is_making_input_list is True:
    mk_init_file_list(INPUT_DIR, RAW_READS, sample_group_name)

# 한줄씩 읽어서 input_path_list에 넣기 
f = open(rf'{INPUT_DIR}{sample_group_name}.txt', 'r')
input_path_list = []
for i in f.readlines():
    input_path_list.append(i[:-1])   
input_path_list = natsort.natsorted(input_path_list)
path_len = len(input_path_list)

print('입력할 paired end reads의 총 수 =', path_len, '\n')
print(input_path_list)

# exit(0) # path list 확인하고 싶으면 이거 풀기

for i in range(path_len):
    if run_mode == 'qc':
        # sp.call(f'fastqc -o {qc_output_dir} -t {qc_threads} --noextract {input_path_list[i]} &', shell=True)
        sp.call(f'echo "fastqc -o {qc_output_dir} -t {qc_threads} --noextract {input_path_list[i]}" \
                    | qsub -N {pbs_N} -o {pbs_o} -j {pbs_j} -l ncpus={pbs_l_core} &', shell=True)
    elif run_mode == 'pp':
        if i%2 == 0: # 짝수면
            process = round(i/path_len, 2) * 100
            print(f'{process}% 진행')

            read1 = input_path_list[i]
            read2 = input_path_list[i+1]
            read_name = input_path_list[i].split('.')[-3].split(r'/')[-1].split(r'_')[-2] # Teratoma-13
            prefix = INPUT_DIR + read_name

            # "ha:b:n:p:i:", ["help", "readA=", "readB=", "readName=", "prefix=", "inputDir="]
            sp.call(f'echo "python {SRC_DIR}processing_RNAseq.py -a {read1} -b {read2} -n {read_name} -p {prefix} -i {INPUT_DIR} \
                    -R {REF_GENOME_DIR} -G {GTF_path} -y {seq_type}" \
                    | qsub -N {pbs_N} -o {pbs_o} -j {pbs_j} -l ncpus={pbs_l_core} &', shell=True)



    
        
