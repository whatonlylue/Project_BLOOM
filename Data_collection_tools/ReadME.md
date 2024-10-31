
# Data Collection Tools

welcome to the data collection tools package from Project BLOOM

#### Dependencies 

Dependencies for this package include:
    
    ncbi_scraper: subprocess, shlex
    genome_scraper: subprocess, shlex, time, concurrent.futures, sys

#### Usecases

ncbi_scraper: script used to find all salmonella accessions and load them onto a text file, must run in order to run genome_scraper, **This script is run in genome_scraper, no need to call it yourself**

genome_scraper: script used to download all salmonella genomes, loads them into a directory inside Data/salmonella_genome_data, reads the script from ncbi_scraper

#### Next Steps

Currently only works for salmonella and the flags for filtering ncbi_scraper are static, same with genome_scraper, looking to add dynamic functionality for both later


