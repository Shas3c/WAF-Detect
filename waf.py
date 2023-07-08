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

#f = os.system('nuclei -silent -nc -target https://bittorrent.com -t technologies/waf-detect.yaml -tags misc')

def banner():
    init()
    banner = f"""
    {Fore.BLUE}		W      W   AAAA   FFFFFF {Style.RESET_ALL}
    {Fore.BLUE}		W      W  A    A  F      {Style.RESET_ALL}
    {Fore.BLUE}		W   W  W  AAAAAA  FFFFF  {Style.RESET_ALL}
    {Fore.BLUE}		 W W W W  A    A  F {Style.RESET_ALL}
    {Fore.BLUE}  		  W   W   A    A  F {Style.RESET_ALL}
      
    {Fore.CYAN} 		      			--- Sahil Sharma (CASB) {Style.RESET_ALL}
    """
    print(banner)

def waf(url, count):
    #url = 'bittorrent.com'
    #count = int()
    time = (datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S")

    command = f"nuclei -silent -nc -target https://{url} -t technologies/waf-detect.yaml -tags misc"

    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    output = result.stdout.strip()
    error = result.stderr.strip()

    #print(output)
    match = re.search(r'waf-detect:(.*?)\]', output)
#print(error)
    if match:
        value=match.group(1)
        #print(value)
        print(f"{url} ---> {Fore.GREEN}{Style.BRIGHT}{value}{Style.RESET_ALL} | {Fore.YELLOW}#{count}{Style.RESET_ALL}  {time}")
        data = [url, 'True', value, (datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S")]
    else:
        print(f"{url} ---> {Fore.RED}No WAF{Style.RESET_ALL} | {Fore.YELLOW}#{count}{Style.RESET_ALL}  {time}")
        data = [url, 'False', '', (datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S")]
    return data
    
if __name__=='__main__':
    banner()
    Threads = 24
    #count=1
    url_list=[]
    with open('/root/Desktop/url.txt','r') as fileobject:
        for url in fileobject:
            url=url.strip()
            url_list.append(url)
    fileobject.close()
    
    list_len = len(url_list)
    
    with open('/root/Desktop/waf-results2.csv','w',newline='') as f:
        writer = csv.writer(f, delimiter=',')
        header = ['Domain','Firewall','Manufacturer', (datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S")]
        writer.writerow(header)
        
        with ThreadPoolExecutor(max_workers=min(Threads, list_len)) as tp:
            for i, x in enumerate(url_list, start=1):
                futures = tp.submit(waf, x, i)
                result = futures.result()
                writer.writerow(result)
        
    
