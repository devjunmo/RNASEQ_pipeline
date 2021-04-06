import subprocess as sp
import glob 
import natsort
from time import sleep

# script형태의 python 파일
# 사용시 hyper parameters에 해당하는 부분 유동적으로 수정
# Input 디렉토리에는 짝이 맞는 paired-end 파일 이외에 어떤것도 존재하지 않아야 함!!

####################### hyper parameters ########################################
threads = 8                                                        	
ref_genome_ver = 'b37'                                              		
prefix = r'/home/jun9485/data/RNASEQ/RNA-seq2/'   
path_list = glob.glob(r'/home/jun9485/data/RNASEQ/RNA-seq2/*')                  		
#################################################################################

path_list = natsort.natsorted(path_list)

path_len = len(path_list)

print('입력할 paired end reads의 총 수 =', path_len)
print(path_list)

usr_input = input('\n 사용할 reads을 확인후, 실행! (y/n)')
usr_input = usr_input.lower()

if usr_input == 'y':
    for i in range(path_len):
        if i%2 == 0: # 짝수면 
            print(f'{path_list[i]} and {path_list[i+1]} mapping start...')
            process = round(i/path_len, 2) * 100
            print(f'{process}% 진행')
            read1 = path_list[i]
            read2 = path_list[i+1]
            read1_name = path_list[i].split('.')[-3].split(r'/')[-1].split(r'_')[-2]
            _prefix = prefix + read1_name + '_'
            sp.call(fr'sh mappingStarPE.sh {read1} {read2} {threads} {ref_genome_ver} {_prefix}', shell=True)
            sleep(3600) # qsub전까지 확실하게 테스트 후 줄것
    print('100% 진행 완료')
else:
    exit(0)

