import os
import subprocess
import re
import csv
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
from threading import Thread
import threading
from colorama import init, Fore, Style
import datetime


def banner():
    init()
    banner = f"""
    {Fore.BLUE}		W      W   AAAA   FFFFFF {Style.RESET_ALL}
    {Fore.BLUE}		W      W  A    A  F      {Style.RESET_ALL}
    {Fore.BLUE}		W   W  W  AAAAAA  FFFFF  {Style.RESET_ALL}
    {Fore.BLUE}		 W W W W  A    A  F {Style.RESET_ALL}
    {Fore.BLUE}  		  W   W   A    A  F {Style.RESET_ALL}
      
    {Fore.CYAN} 		      			--- Sahil Sharma (Shas3c) {Style.RESET_ALL}
    """
    print(banner)

def waf(url, count):

    command = f"nuclei -silent -nc -target https://{url} -t technologies/waf-detect.yaml -tags misc"

    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    output = result.stdout.strip()
    
    match = re.search(r'waf-detect:(.*?)\]', output)

    if match:
        value=match.group(1)
        
        print(f"{url} ---> {Fore.GREEN}{Style.BRIGHT}{value}{Style.RESET_ALL} | {Fore.YELLOW}#{count}{Style.RESET_ALL}")
        data = [url, 'True', value]
    else:
        print(f"{url} ---> {Fore.RED}No WAF{Style.RESET_ALL} | {Fore.YELLOW}#{count}{Style.RESET_ALL}  {time}")
        data = [url, 'False', '']
    return data
    
if __name__=='__main__':
    banner()
    Threads = 4                        # Change threads according to your system requirements

    input_path = 'url.txt'             # pass the full path of your input file
    output_path = 'waf-results.csv'    #pass the full path of output file generation
    
    url_list=[]
    with open(input_path,'r') as fileobject:
        for url in fileobject:
            url=url.strip()
            url_list.append(url)
    fileobject.close()
    
    list_len = len(url_list)
    
    with open(output_path,'w',newline='') as f:
        writer = csv.writer(f, delimiter=',')
        header = ['Domain','Firewall','Manufacturer']
        writer.writerow(header)
        
        with ThreadPoolExecutor(max_workers=min(Threads, list_len)) as tp:
            for i, x in enumerate(url_list, start=1):
                futures = tp.submit(waf, x, i)
                result = futures.result()
                writer.writerow(result)
        
    
