
import shlex
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import sys





accession_list = []
sdf = open('../Data/salmonella_data.txt','r')
while True:
    accession = sdf.readline()

    if not accession:
        break
    else:
        accession = accession.split("%")
        if accession[2].strip() != "Null":
            accession_list.append(accession[1])
sdf.close()
genome_download = []
accession_list_count = len(accession_list) - 1
start = time.time()


#making a process to be parallelized 

def download_data(accession: str, index: int) -> str:
    
    genome_cmd = f"datasets download genome accession {accession} --filename {index}_salmonella_{accession}.zip --include genome,protein"
    genome_cmd = shlex.split(genome_cmd)

    res = subprocess.run(genome_cmd, cwd="../Data/salmonella_genome_data/", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if res.returncode != 0:
        return f"Error downloading genome {accession}"
    return "Success downloading genome {accession}"


with ThreadPoolExecutor(max_workers=190) as executor:
    futures = [executor.submit(download_data, accession, i) for i,accession in enumerate(accession_list)]
    
    for i, future in enumerate(as_completed(futures),0):


        percent = int((i / accession_list_count) * 100)
        dash_string = "-" * (100 - percent)
        complete_string = "#" * (percent)
        curr_time = float(time.time() - start)
        

        print(chr(27)+"[2J")
        print("Downloading "+accession_list[i]+ " dataset, "+str(i)+"/"+str(accession_list_count) + " Time Elapsed: "+str(curr_time))
        print("Process: ["+ (complete_string + dash_string) +"] "+ str(percent) +"%")   




    
print("Process Completed")
print("All genome data downloaded to Data/salmonella_genome_data")

