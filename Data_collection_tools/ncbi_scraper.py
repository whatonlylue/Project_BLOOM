import subprocess
import shlex


def run():
    data_call = "datasets summary genome taxon 'Salmonella' --assembly-level complete --as-json-lines"
    format_call = "dataformat tsv genome --fields accession,assminfo-biosample-serovar"

    data_call = shlex.split(data_call)
    format_call = shlex.split(format_call)


    data_process = subprocess.Popen(data_call, stdout=subprocess.PIPE)
    format_process = subprocess.run(format_call, stdin=data_process.stdout, capture_output=True,text=True)

    data_process.stdout.close()


    with open('../Data/salmonella_data.txt', 'w') as sdf:
    
        data_to_write = (format_process.stdout).split("\n")
        i = 0
        
        count = len(data_to_write)

        for line in data_to_write:
            check = line.split("\t")

            if len(check) < 2:
                pass
        
            else:
            
                if not check[1]:
                    check[1] += "Null"
                elif "not available:" in check[1]:
                    check[1] = "Null"
                elif "missing" in check[1]:
                    check[1] = "Null"
                elif "Not Applicable" in check[1]:
                    check[1] = "Null"
                elif "Not known" in check[1]:
                    check[1] = "Null"
            
                sdf.write(str(i)+"%"+check[0]+"%"+check[1]+"\n")
            i+=1
            print(chr(27) + "[2J")
            percent = int(float(i / count)) * 100
        
            not_yet = '-' * (100 - percent)
            done = '#' * percent
            print("Collecting Salmonella and writing to salmonella_data.txt")
            print("Progress: ["+(done+not_yet)+"] "+str(percent)+"%")

        

    print("Process Complete")




