import shutil
import shlex
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import threading
import zipfile
from ncbi_scraper import run



def is_conda_env_active() -> bool:
    """
    Checks if conda environment 'ncbi_datasets' is active.

    :returns: True if environment is active, false otherwise. 
    """

    return 'CONDA_DEFAULT_ENV' in os.environ and os.environ['CONDA_DEFAULT_ENV'] == 'ncbi_datasets' 

def accesion_list_maker() -> list[str]:
    """
    Opens salmonella_data.txt generated from ncbi_scraper, pulls list of accession files.

    :returns: list of accession file names in string format.
    """
    accession_list = []
    sdf = open('../Data/salmonella_data.txt','r') #Opens data file
    while True:
        accession = sdf.readline()

        if not accession:
            break
        else:
            accession = accession.split("%")
            if accession[2].strip() != "Null": #if accessions serovar is null, it excludes it from list
                accession_list.append(accession[1])
    sdf.close()
    return accession_list


def download_data_and_unzip(accession: str, index: int, retires=3) -> str:
    """
    Method desined to run a download script for the specified accesion, 
    unzips downloaded accession and filters by '.fna'.

    :param accesion: String of accession file namelist
    :param index: Integer of current file count (used to keep downloads unique)
    :param retries: Amount of attemps to download file before moving to the next
    :returns: String indicator of current progress
    :raises zipfile.BadZipFile: Skips if file cannot be unzipped 
    :raises FileNotFoundError: Skips if file not found for removal
    """


    filename = f"{index}_salmonella_{accession}.zip"
    filepath = f"../Data/salmonella_genome_data/{filename}"

    genome_cmd = f"datasets download genome accession {accession} --filename {filename} --include genome" #ncbi_dataset api call to download accession genome
    genome_cmd = shlex.split(genome_cmd)
    
    for attempt in range(retires):
        res = subprocess.run(genome_cmd, cwd="../Data/salmonella_genome_data/", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) 
        if res.returncode == 0:
            break
        time.sleep(1)
    else:
        return f"Error downloading genome {accession} after {retires} attemps"
    
    #Make a temporary directory in order to move files into salmonella_genome_data/, deletes temp directory afterwards
    temp_extract_path = f"../Data/salmonella_genome_data/temp_{accession}/"
    os.makedirs(temp_extract_path, exist_ok=True)

    try:
        with zipfile.ZipFile(filepath,'r') as zip_ref:
            
            for f in zip_ref.namelist(): 
                if f.endswith(".fna"):
                    zip_ref.extract(f, path=temp_extract_path)
                    # Move and rename the extracted .fna file to the final target directory
                    extracted_file = os.path.join(temp_extract_path, f)
                    target_path = f"../Data/salmonella_genome_data/{accession}.fna"
                    shutil.move(extracted_file, target_path)

        os.remove(filepath)

        return f"Downloaded and unzipped {accession}"
    except zipfile.BadZipFile:
        return f"Failed to unzip {filename}: Bad Zip File"
    except FileNotFoundError:
        return f"File not found for removal: {filename}"
    finally:
        shutil.rmtree(temp_extract_path, ignore_errors=True)
    return "Success"



def parallelized_downloads(accession_list: list[str], start: float) -> None:
    """
    Parallezies download_data_and_unzip so that multiple downloads can be preformed at once

    :param accession_list: list of every accesion file found from accesion_list_maker()
    :param start: float of time used to track download time

    """
    accession_list_count = len(accession_list) - 1 
    with ThreadPoolExecutor(max_workers=(4*os.cpu_count())) as executor: #Scales max workers based on amount of cpu cores
        futures = [executor.submit(download_data_and_unzip, accession, i) for i,accession in enumerate(accession_list)]
    
        for i, future in enumerate(as_completed(futures),0):
            
            with threading.Lock(): #Locks threading to keep counter somewhat accurate
                percent = int((i / accession_list_count) * 100)
            
            dash_string = "-" * (100 - percent)
            complete_string = "#" * (percent)
            curr_time = float(time.time() - start)
        

            print(chr(27)+"[2J")
            print(f"Downloading {accession_list[i]} dataset, {i}/{accession_list_count} Time Elapsed: {curr_time:.2f} seconds")
            print(f"Process: [{complete_string + dash_string}] {percent}%")   


def main():
    if not is_conda_env_active():
        raise Exception("The conda environment 'ncbi_datasets', needs to be active to run this script")
    if not os.path.exists("../Data/salmonella_data.txt"):
        print("Salmonella_data.txt, not found, building file")
        run()

    accession_list = accesion_list_maker()

    parallelized_downloads(accession_list, time.time())
    
    print("Process Completed")
    print("All genome data downloaded to Data/salmonella_genome_data")

if __name__ == '__main__':
    main()
