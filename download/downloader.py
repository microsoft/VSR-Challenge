# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import os
import requests
import time
import argparse
from concurrent.futures import ThreadPoolExecutor

def download_file(url, download_dir):
    local_path = url.split('vsr-challenge/')[-1]
    print('Downloading: ', local_path)
    os.makedirs(os.path.join(download_dir, "/".join(local_path.split('/')[:-1])), exist_ok=True)
    r = requests.get(url, stream=True)
    with open(os.path.join(download_dir, local_path), 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    time.sleep(1)

def download_files(file_list, download_dir):
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    with open(file_list, 'r') as f:
        lines = f.readlines()
        urls = [line.strip() for line in lines]

    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(lambda url: download_file(url, download_dir), urls)

    print('Download complete')

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Utility script to download files from a list of URLs')    
    parser.add_argument("--list-of-files", required=True,
                        help="List of files to download")
    parser.add_argument("--local-path", required=True,
                        help="Local path to download the files to")
    args = parser.parse_args()

    download_files(args.list_of_files, args.local_path)
