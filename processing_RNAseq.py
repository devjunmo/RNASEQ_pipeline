import subprocess as sp
import glob
import natsort
import time
import sys
import getopt
import os


####################### hyper parameters ####################################################

# 디버깅모드시 실행파일은 주석처리, 중간생성물 지우기 여부는 False처리, max_looping=1 처리!!

THREADS = 1                                   


sorting_order = 'coordinate' # or queryname

max_looping = 1

##############################################################################################

read1 = ''
read2 = ''
read_name = ''
prefix = ''
INPUT_DIR = ''
REF_GENOME_DIR = ''
GTF_FILE_PATH = ''
seq_type = ''

def rm_file(is_rm, file):
    if is_rm is True:
        try:
            os.remove(file)
        except FileNotFoundError:
            print(f'{file} 파일이 존재하지 않아 삭제하지 못함')

def main(argv):
    file_name = argv[0]
    global read1
    global read2
    global read_name
    global prefix
    global INPUT_DIR
    global REF_GENOME_DIR
    global GTF_FILE_PATH
    global seq_type

    try:
        opts, etc_args = getopt.getopt(argv[1:], "ha:b:n:p:i:R:L:y:", ["help", "readA=", "readB=", "readName=", "prefix=", "inputDir=",\
            "ref=", "gtf=", "type="])

    except getopt.GetoptError:  # 옵션지정이 올바르지 않은 경우
        print(file_name, 'option error')
        sys.exit(2)

    for opt, arg in opts:  # 옵션이 파싱된 경우
        print(opt)
        if opt in ("-h", "--help"):  # HELP 요청인 경우 사용법 출력
            print(file_name, 'file name..')
            sys.exit(0)

        elif opt in ("-a", "--readA"):  # 인스턴명 입력인 경우
            read1 = arg
        elif opt in ("-b", "--readB"):
            read2 = arg
        elif opt in ("-n", "--readName"):
            read_name = arg
        elif opt in ("-p", "--prefix"):
            prefix = arg
        elif opt in ("-i", "--inputDir"):
            INPUT_DIR = arg
        elif opt in ("-R", "--ref"):
            REF_GENOME_DIR = arg
        elif opt in ("-G", "--gtf"):
            GTF_FILE_PATH = arg
        elif opt in ("-y", "--type"):
            seq_type = arg

main(sys.argv)

error_log_file = INPUT_DIR + "errorLog.txt"



# mapping
mapping_dir = INPUT_DIR + r'mapped/'
output_prefix = mapping_dir + read_name + '_'

if not os.path.isdir(mapping_dir):
    os.mkdir(mapping_dir)

loop_count = 0

while True:
    try:
        mapping_time = time.time()
        err_msg = f'An_error_occurred_in_mappingStarPE.sh:_Mapping_reads_was_failed.{read_name}'
        # sp.check_call(fr'sh mappingStarPE.sh {read1} {read2} {THREADS} {REF_GENOME_DIR} {output_prefix}', shell=True)
        break

    except sp.CalledProcessError as e:
        sp.call(f'sh write_log.sh {err_msg} {error_log_file}', shell=True)
        loop_count += 1
        if loop_count > max_looping:
            exit(0)


# read count

bam_file = output_prefix + r'Aligned.sortedByCoord.out.bam'
count_dir = mapping_dir + r'count/'

if not os.path.isdir(count_dir):
    os.mkdir(count_dir)

while True:
    try:
        mapping_time = time.time()
        err_msg = f'An_error_occurred_in_htseq_count.sh:_Counting_reads_was_failed.{read_name}'
        sp.check_call(fr'sh htseq_count.sh {bam_file} {GTF_FILE_PATH} {count_dir}', shell=True)
        break

    except sp.CalledProcessError as e:
        #sp.call(f'sh write_log.sh {err_msg} {error_log_file}', shell=True)
        loop_count += 1
        if loop_count > max_looping:
            exit(0)
