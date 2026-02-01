import argparse
import os
import random
import requests
import requests_raw
import string
import time
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from concurrent.futures import ThreadPoolExecutor

input_file = 'input'
output_file = 'output'
MAX_THREADS = 200

HTTP_PROXY = {
    "http":"http://127.0.0.1:8080",
    "https":"http://127.0.0.1:8080"
}

def checkArguments():
    global input_file
    global output_file

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=str, required=True, help="Input file")
    parser.add_argument("-o", "--output",type=str, default="output", help="Output file")

    args = parser.parse_args()
    
    input_file = args.input
    output_file = args.output

def get_hosts():
    global input_file
    hosts = []

    with open(input_file) as f:
        lines = f.readlines()
        for host in lines:
            hosts.append(host.strip())
    f.close()
    return hosts

def generate_request(hosts_request_type):
    try:
        host = hosts_request_type.split("|")[0]
        type = hosts_request_type.split("|")[1]
        cache_buster = hosts_request_type.split("|")[2]

        if type == 'base':
            raw_request = b"GET /" + cache_buster.encode() + b".js?cache_buster=" + cache_buster.encode() + b" HTTP/1.1\r\nHost: " + host.encode() + b"\r\nUser-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36\r\nAccept: */*\r\nAccept-Language: en-US,en;q=0.9\r\n\r\n"
            
            #response = requests_raw.raw(url=("https://" + host), data=raw_request, verify=False, proxies=None, allow_redirects=False, timeout=5)
            response = requests_raw.raw(url=("https://" + host), data=raw_request, verify=False, proxies=HTTP_PROXY, allow_redirects=False, timeout=5)

            print(host + "/" + cache_buster + ".js?cache_buster=" + cache_buster, response.status_code)
            #print(response.text)
        else:
            raw_request = b"GET /" + cache_buster.encode() + b".js?cache_buster=" + cache_buster.encode() + b" HTTP/1.1\r\nHost: " + host.encode() + b"\r\nX-Forwarded-Proto: http\r\nUser-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36\r\nAccept: */*\r\nAccept-Language: en-US,en;q=0.9\r\n\r\n"
            
            #response = requests_raw.raw(url=("https://" + host), data=raw_request, verify=False, proxies=None, allow_redirects=False, timeout=5)
            response = requests_raw.raw(url=("https://" + host), data=raw_request, verify=False, proxies=HTTP_PROXY, allow_redirects=False, timeout=5)

            print(host + "/" + cache_buster + ".js?cache_buster=" + cache_buster, response.status_code)
            #print(response.text)

    except Exception as e:
        print('Request failed due to error:', e)

if __name__ == '__main__':
    s = time.perf_counter()

    checkArguments()

    hosts = get_hosts()

    hosts_request_types = []

    for host in hosts:
        hosts_request_types.append(host + "|base" + "|testcheck")

        cache_buster = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))

        for i in range(1):
            hosts_request_types.append(host + "|modified" + "|" + cache_buster)

    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        executor.map(generate_request, hosts_request_types)

    elapsed = time.perf_counter() - s    
    
    print(f"Execution time: {elapsed:0.2f} seconds")
