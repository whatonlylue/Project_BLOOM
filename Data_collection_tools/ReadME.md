
# Data Collection Tools

welcome to the data collection tools package from Project BLOOM, these tools are used to collect all genome data and create embed vectors for each of them

#### Usecases

ncbi_scraper:
```python
run() -> None: #Writes all Salmonella Genomic names from ncbi_datasets to salmonella_data.txt
```

genome_scraper:
```python
is_conda_env_active() -> bool: #Checks if your environment is correct in order to run
accesion_list_maker() -> list[str]: #Creates a list of all genomic accessions collected in salmonella_data.txt
download_data_and_unzip(accesion: str, index: int, retires=3) -> str: #This is the subprocess function used to parallelize this process, this finds the genome file based on accesion, downloads it from ncbi_datasets, then exctracts the unzip file
parallelized_downloads(accession_list: list[str] start:float) -> None: #Uses ThreadPoolExecutor inorder to download and unzip all genome files in parallel
```

#### Next Steps

Currently only works for salmonella and the flags for filtering ncbi_scraper are static, same with genome_scraper, looking to add dynamic functionality for both later


